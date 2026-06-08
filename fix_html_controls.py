import re

with open("index.html", "r") as f:
    html = f.read()

# Add 'controls' to video tags
# Since we stripped 'controls' before, we just add it back.
html = re.sub(r'<video playsinline loop', '<video playsinline controls loop', html)

# Remove the CSS hiding controls
css_to_remove = """        /* Hide all video controls and loading spinners */
        video::-webkit-media-controls { display: none !important; }
        video::-webkit-media-controls-enclosure { display: none !important; }
        video::-webkit-media-controls-panel { display: none !important; }"""
html = html.replace(css_to_remove, '')

# Now replace the JS logic
old_js_start = "// Hover to play paradigm"
end_of_script = "        });\n    </script>"

if old_js_start in html:
    start_idx = html.find(old_js_start)
    end_idx = html.find(end_of_script) + len("        });")
    
    new_js = """// Click to play paradigm
        videos.forEach(video => {
            const parent = video.parentElement;
            
            const onClick = function() {
                video.play();
                // 播放后解绑点击，不再干扰用户
                parent.removeEventListener('click', onClick);
            };

            parent.addEventListener('click', onClick);
        });"""
        
    html = html[:start_idx] + new_js + html[end_idx:]

with open("index.html", "w") as f:
    f.write(html)
