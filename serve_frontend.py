#!/usr/bin/env python3
"""
Simple HTTP server to serve the frontend and proxy API calls to the backend.
"""
import http.server
import socketserver
import os
import sys
from pathlib import Path

# Get the frontend directory
FRONTEND_DIR = Path(__file__).parent / "frontend"
PORT = 8000

class FrontendHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(FRONTEND_DIR), **kwargs)
    
    def end_headers(self):
        # Add CORS headers
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()
    
    def log_message(self, format, *args):
        print(f"[{self.client_address[0]}] {format % args}")

if __name__ == "__main__":
    os.chdir(FRONTEND_DIR)
    
    with socketserver.TCPServer(("", PORT), FrontendHandler) as httpd:
        print(f"🚀 Frontend server running at http://127.0.0.1:{PORT}")
        print(f"📁 Serving files from: {FRONTEND_DIR}")
        print(f"🔗 Backend available at http://127.0.0.1:8007")
        print("\nPress Ctrl+C to stop the server")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n✅ Server stopped")
            sys.exit(0)
