#!/usr/bin/env python3
"""
Local web server for Godot HTML5 export.
Serves with required CORS headers for SharedArrayBuffer (if threaded)
and proper MIME types for .wasm/.pck files.

Usage: python serve.py [port]
Default port: 8080
"""
import http.server
import sys
import os
import webbrowser

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8080
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class GodotHTTPHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    extensions_map = {
        **http.server.SimpleHTTPRequestHandler.extensions_map,
        '.wasm': 'application/wasm',
        '.pck': 'application/octet-stream',
        '.js': 'application/javascript',
    }

    def end_headers(self):
        # Required for SharedArrayBuffer (threaded builds)
        self.send_header('Cross-Origin-Opener-Policy', 'same-origin')
        self.send_header('Cross-Origin-Embedder-Policy', 'require-corp')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Cache-Control', 'no-cache')
        super().end_headers()

if __name__ == '__main__':
    os.chdir(DIRECTORY)
    with http.server.HTTPServer(('0.0.0.0', PORT), GodotHTTPHandler) as httpd:
        url = f"http://localhost:{PORT}/index.html"
        print(f"\n{'='*50}")
        print(f"  Word Bloom Web Demo")
        print(f"  URL: {url}")
        print(f"  Press Ctrl+C to stop")
        print(f"{'='*50}\n")
        webbrowser.open(url)
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped.")
