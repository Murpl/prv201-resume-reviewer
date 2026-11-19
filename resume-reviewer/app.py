"""Small loopback-only web server. Run: python app.py"""
import base64
import binascii
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from reviewer import analyze, extract_pdf, ReviewError, MAX_PDF

ROOT = Path(__file__).resolve().parent

class Handler(BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass  # Do not log resume contents or request paths.

    def send(self, code, payload, content_type='application/json'):
        data = json.dumps(payload).encode() if content_type == 'application/json' else payload
        self.send_response(code)
        self.send_header('Content-Type', content_type)
        self.send_header('Content-Length', str(len(data)))
        self.send_header('Cache-Control', 'no-store')
        self.send_header('X-Content-Type-Options', 'nosniff')
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        if self.path == '/':
            self.send(200, (ROOT / 'index.html').read_bytes(), 'text/html; charset=utf-8')
        elif self.path == '/sample':
            self.send(200, {'resume': (ROOT / 'samples/resume.txt').read_text(),
                            'job': (ROOT / 'samples/job.txt').read_text()})
        else:
            self.send(404, {'error': 'Not found'})

    def do_POST(self):
        if self.path not in ['/extract', '/analyze']:
            self.send(404, {'error': 'Not found'})
            return
        # Reject browser requests initiated by foreign origins.
        if self.headers.get('Origin') not in [None, 'http://127.0.0.1:8765', 'http://localhost:8765']:
            self.send(403, {'error': 'Only the local app may submit documents.'})
            return
        try:
            length = int(self.headers.get('Content-Length', '0'))
            if not 0 < length <= MAX_PDF * 2:
                raise ReviewError('Request is empty or too large.')
            if self.headers.get('Content-Type', '').split(';')[0] != 'application/json':
                raise ReviewError('Expected JSON input.')
            body = json.loads(self.rfile.read(length))
            if not isinstance(body, dict):
                raise ReviewError('Expected an input object.')
            if self.path == '/extract':
                data = base64.b64decode(body.get('pdf', ''), validate=True)
                result = {'text': extract_pdf(data)}
            else:
                result = analyze(body.get('resume', ''), body.get('job', ''),
                                 body.get('mode', 'local'), body.get('model', 'qwen2.5:3b'))
            self.send(200, result)
        except (ReviewError, ValueError, TypeError, binascii.Error) as exc:
            self.send(400, {'error': str(exc)})
        except Exception:
            self.send(500, {'error': 'Unexpected processing error. Please try a smaller text-based resume.'})

if __name__ == '__main__':
    print('Resume Review is running at http://127.0.0.1:8765. Press Ctrl+C to stop.')
    ThreadingHTTPServer(('127.0.0.1', 8765), Handler).serve_forever()
