"""One fixed response on loopback; never serves repository files."""
from http.server import BaseHTTPRequestHandler, HTTPServer


class Probe(BaseHTTPRequestHandler):
    def do_GET(self):
        body = b'hath-relay-loopback-proof-20261030\n'
        self.send_response(200 if self.path == '/probe' else 404)
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)


if __name__ == '__main__':
    with HTTPServer(('127.0.0.1', 39082), Probe) as server:
        server.timeout = 60
        print('READY 127.0.0.1:39082, one request or 60s timeout', flush=True)
        server.handle_request()
