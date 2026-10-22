"""
Vercel Serverless Function Entrypoint for PhishShift Message Risk Scanner.
Exposes WSGI callable `app` and `handler` for Vercel Python Runtime.
Includes resilient diagnostic reporting so import/runtime issues are visibly surfaced.
"""
import sys
import traceback
from pathlib import Path

# Setup paths to ensure root, api, src, and web are importable
CURRENT_DIR = Path(__file__).resolve().parent
ROOT_DIR = CURRENT_DIR.parent

for p in [ROOT_DIR, CURRENT_DIR, ROOT_DIR / "src", ROOT_DIR / "web"]:
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

app = None
handler = None

try:
    from web.app import app as flask_app
    app = flask_app
    handler = flask_app
except Exception as e:
    startup_error = traceback.format_exc()
    print("Vercel Startup Error Traceback:\n", startup_error)

    def diagnostic_app(environ, start_response):
        status = '200 OK'
        headers = [('Content-Type', 'text/html; charset=utf-8')]
        start_response(status, headers)
        html = f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>PhishShift Vercel Diagnostic</title>
  <style>
    body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #060913; color: #f1f5f9; padding: 2rem; line-height: 1.6; }}
    .card {{ background: #0f172a; border: 1px solid #ef4444; border-radius: 12px; padding: 2rem; max-width: 900px; margin: 2rem auto; box-shadow: 0 10px 30px rgba(0,0,0,0.5); }}
    h1 {{ color: #ef4444; font-size: 1.5rem; margin-top: 0; }}
    pre {{ background: #020617; padding: 1.25rem; border-radius: 8px; color: #fca5a5; overflow-x: auto; font-size: 13px; border: 1px solid #991b1b; }}
    code {{ color: #38bdf8; }}
  </style>
</head>
<body>
  <div class="card">
    <h1>PhishShift Vercel Startup Diagnostic</h1>
    <p>A Python exception occurred while initializing the application on Vercel:</p>
    <pre>{startup_error}</pre>
    <h3>Environment:</h3>
    <p><strong>Python Version:</strong> <code>{sys.version}</code></p>
    <p><strong>Current Directory:</strong> <code>{Path.cwd()}</code></p>
    <p><strong>sys.path:</strong> <code>{sys.path}</code></p>
  </div>
</body>
</html>"""
        return [html.encode("utf-8")]

    app = diagnostic_app
    handler = diagnostic_app

if __name__ == "__main__":
    if hasattr(app, "run"):
        app.run(host="127.0.0.1", port=5000, debug=True)
