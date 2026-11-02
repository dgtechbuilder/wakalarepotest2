"""Build a single-file copy of the game with every asset embedded (used for the Claude artifact).
Usage: python3 tools/build_standalone.py [out.html]   (default: dist/wakala-game.html)"""
import base64, json, os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, 'dist', 'wakala-game.html')
src = open(os.path.join(ROOT, 'index.html'), encoding='utf-8').read()
head = re.search(r'<head>(.*)</head>', src, re.S).group(1)
body = re.search(r'<body>(.*)</body>', src, re.S).group(1)
head = re.sub(r'<meta charset[^>]*>\s*', '', head)
head = re.sub(r'<meta name="viewport"[^>]*>\s*', '', head)
title = re.search(r'<title>.*?</title>', head).group(0)
head = head.replace(title, '')
assets, d = {}, os.path.join(ROOT, 'assets')
for f in sorted(os.listdir(d)):
    name, ext = os.path.splitext(f)
    mime = 'image/png' if ext == '.png' else 'image/jpeg'
    assets[name] = f'data:{mime};base64,' + base64.b64encode(open(os.path.join(d, f), 'rb').read()).decode()
marker = '<script>\n/* ---------- farm renderer'
assert marker in body, 'renderer script marker not found'
body = body.replace(marker, '<script>window.ASSETS=' + json.dumps(assets) + ';</script>\n' + marker, 1)
os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
open(out, 'w', encoding='utf-8').write(title + '\n<meta name="claude:viewport-fit-sides" content="cover">\n' + head.strip() + '\n' + body)
print(f'wrote {out} ({os.path.getsize(out) / 1e6:.1f} MB)')
