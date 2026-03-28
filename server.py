import http.server
import socketserver
import os
import urllib.parse

PORT = 8000  # 修改为未占用的端口
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class AILINKHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        # 去掉开头的 '/'
        relative_path = path.lstrip('/')
        if not relative_path:
            relative_path = 'index.html'

        full_path = os.path.join(BASE_DIR, relative_path)
        if os.path.isfile(full_path):
            ext = os.path.splitext(full_path)[1].lower()
            if ext == '.js':
                self.send_response(200)
                self.send_header('Content-Type', 'application/javascript')
                self.end_headers()
                with open(full_path, 'rb') as f:
                    self.wfile.write(f.read())
                return
            else:
                self.path = path
                return super().do_GET()
        else:
            # 文件不存在，返回 index.html（SPA 回退）
            index_path = os.path.join(BASE_DIR, 'index.html')
            if os.path.isfile(index_path):
                self.send_response(200)
                self.send_header('Content-Type', 'text/html')
                self.end_headers()
                with open(index_path, 'rb') as f:
                    self.wfile.write(f.read())
                return
            else:
                self.send_error(404, 'File Not Found')
                return

if __name__ == '__main__':
    # 允许重用地址，避免因 TIME_WAIT 导致端口占用
    socketserver.TCPServer.allow_reuse_address = True
    try:
        with socketserver.TCPServer(("", PORT), AILINKHandler) as httpd:
            print(f"Serving AILINK project at http://localhost:{PORT}")
            print("Press Ctrl+C to stop")
            httpd.serve_forever()
    except OSError as e:
        if e.errno == 98:
            print(f"Error: Port {PORT} is already in use. Please stop the program using that port or change PORT in the script.")
        else:
            raise