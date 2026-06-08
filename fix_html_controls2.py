with open("index.html", "r") as f:
    html = f.read()

start_marker = "        // Hover to play paradigm"
end_marker = "    </script>"

start_idx = html.find(start_marker)
end_idx = html.find(end_marker, start_idx)

if start_idx != -1 and end_idx != -1:
    new_js = """        // Click to play paradigm
        videos.forEach(video => {
            const parent = video.parentElement;
            
            const onClick = function() {
                video.play();
                // 播放后解绑点击，不再干扰用户
                parent.removeEventListener('click', onClick);
            };

            parent.addEventListener('click', onClick);
        });
        });
"""
    html = html[:start_idx] + new_js + html[end_idx:]

with open("index.html", "w") as f:
    f.write(html)
