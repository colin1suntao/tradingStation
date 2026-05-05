#!/usr/bin/env python3
"""
简单的前端静态文件服务器
"""

from http.server import HTTPServer, SimpleHTTPRequestHandler
import os
import sys

# CORS 处理
class CORSRequestHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

def main():
    # 切换到 frontend 目录
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    port = 3000
    server_address = ('0.0.0.0', port)
    httpd = HTTPServer(server_address, CORSRequestHandler)
    
    print(f"🎉 TradingStation 前端服务器已启动!")
    print(f"📱 访问地址: http://localhost:{port}")
    print(f"🔄 按 Ctrl+C 停止服务器")
    print("-" * 50)
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n👋 服务器已停止")
        httpd.shutdown()

if __name__ == "__main__":
    main()
