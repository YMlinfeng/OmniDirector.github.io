import re

with open("index.html", "r") as f:
    html = f.read()

# Task 1: Fix overall.png caching
html = re.sub(r'src="image/overall\.png(\?v=\d+)?"', 'src="image/overall.png?v=2"', html)

# Task 2: Remove 'controls' from video tags
html = html.replace(' controls ', ' ')
html = html.replace('controls ', ' ')

# Remove the old hover/click script
old_script_start = "videos.forEach(video => {"
old_script_end_idx = html.find("</script>", html.find(old_script_start))
if old_script_start in html and old_script_end_idx != -1:
    before_script = html[:html.find(old_script_start)]
    after_script = html[old_script_end_idx:]
    
    new_script = """
        // Password Protection
        const overlay = document.getElementById('password-overlay');
        const passInput = document.getElementById('password-input');
        const passSubmit = document.getElementById('password-submit');
        const passError = document.getElementById('password-error');

        function checkPassword() {
            if (passInput.value === 'klingcamera') {
                overlay.style.display = 'none';
                document.body.style.overflow = 'auto';
            } else {
                passError.style.display = 'block';
            }
        }

        if (overlay) {
            passSubmit.addEventListener('click', checkPassword);
            passInput.addEventListener('keypress', function(e) {
                if (e.key === 'Enter') checkPassword();
            });
            document.body.style.overflow = 'hidden';
        }

        // Hover to play paradigm
        videos.forEach(video => {
            const parent = video.parentElement;
            
            parent.addEventListener('mouseenter', () => {
                video.preload = 'auto';
                let playPromise = video.play();
                if (playPromise !== undefined) {
                    playPromise.catch(error => {
                        // Auto-play was prevented
                    });
                }
            });

            parent.addEventListener('mouseleave', () => {
                video.pause();
                // To completely free the video and show the poster again
                video.removeAttribute('src'); 
                video.load(); 
                // Re-add the src so it can be played again next time
                video.setAttribute('src', video.getAttribute('data-original-src') || video.currentSrc);
            });
            
            // Save original src
            if (!video.getAttribute('data-original-src')) {
                video.setAttribute('data-original-src', video.getAttribute('src'));
            }
        });
    """
    html = before_script + new_script + after_script

# Wait, `video.removeAttribute('src')` and `video.load()` is the most robust way to stop downloading, 
# but it might cause the video to go black if poster isn't re-fetched.
# Let's refine the hover script to just pause and reset time. 
# Re-writing the script part to be safer:
new_script_safer = """
        // Password Protection
        const overlay = document.getElementById('password-overlay');
        const passInput = document.getElementById('password-input');
        const passSubmit = document.getElementById('password-submit');
        const passError = document.getElementById('password-error');

        function checkPassword() {
            if (passInput.value === 'klingcamera') {
                overlay.style.display = 'none';
                document.body.style.overflow = 'auto';
            } else {
                passError.style.display = 'block';
            }
        }

        if (overlay) {
            passSubmit.addEventListener('click', checkPassword);
            passInput.addEventListener('keypress', function(e) {
                if (e.key === 'Enter') checkPassword();
            });
            document.body.style.overflow = 'hidden';
        }

        // Hover to play paradigm
        videos.forEach(video => {
            const parent = video.parentElement;
            
            parent.addEventListener('mouseenter', () => {
                video.preload = 'auto';
                let playPromise = video.play();
                if (playPromise !== undefined) {
                    playPromise.catch(error => {});
                }
            });

            parent.addEventListener('mouseleave', () => {
                video.pause();
                video.currentTime = 0;
                video.load(); // This stops the current buffer and resets to poster
            });
        });
    """

if old_script_start in html and old_script_end_idx != -1:
    html = before_script + new_script_safer + after_script

# Add password overlay right after <body>
password_overlay_html = """
    <div id="password-overlay" style="position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background: #17181a; z-index: 99999; display: flex; flex-direction: column; align-items: center; justify-content: center;">
        <img src="image/logo.png" alt="Logo" style="height: 60px; margin-bottom: 20px;" />
        <h2 style="color: white; margin-bottom: 20px; font-weight: 300;">Private Debug Mode</h2>
        <input type="password" id="password-input" placeholder="Enter password" style="padding: 10px; font-size: 16px; border-radius: 5px; border: 1px solid #333; margin-bottom: 10px; background: #222; color: #fff; width: 250px; text-align: center; outline: none;">
        <button id="password-submit" style="padding: 10px 20px; font-size: 16px; cursor: pointer; border-radius: 5px; background: #fff; color: #000; border: none; font-weight: bold; width: 250px; transition: background 0.3s;">Verify</button>
        <p id="password-error" style="color: #ff5252; display: none; margin-top: 10px;">Incorrect password</p>
    </div>
"""
if '<div id="password-overlay"' not in html:
    html = html.replace('<body>', '<body>\n' + password_overlay_html)

# Also let's hide any native spinner via CSS. Webkit has pseudo elements for this.
css_injection = """
        /* Hide all video controls and loading spinners */
        video::-webkit-media-controls { display: none !important; }
        video::-webkit-media-controls-enclosure { display: none !important; }
        video::-webkit-media-controls-panel { display: none !important; }
"""
if "video::-webkit-media-controls-enclosure" not in html:
    html = html.replace('</style>', css_injection + '\n    </style>')

with open("index.html", "w") as f:
    f.write(html)
