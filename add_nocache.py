import re

with open("index.html", "r") as f:
    html = f.read()

nocache_tags = """
    <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
    <meta http-equiv="Pragma" content="no-cache">
    <meta http-equiv="Expires" content="0">
"""

if "Cache-Control" not in html:
    html = html.replace('<head>', '<head>\n' + nocache_tags)

with open("index.html", "w") as f:
    f.write(html)
