with open("index.html", "r") as f:
    html = f.read()

html = html.replace('});\n    </script>', '});\n        });\n    </script>')
with open("index.html", "w") as f:
    f.write(html)
