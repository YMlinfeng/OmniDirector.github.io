with open("index.html", "r") as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    if "});html>" in line:
        new_lines.append("        });\n")
        new_lines.append("        });\n")
        new_lines.append("    </script>\n")
        new_lines.append("</body>\n")
        new_lines.append("</html>\n")
        break
    new_lines.append(line)

with open("index.html", "w") as f:
    f.writelines(new_lines)
