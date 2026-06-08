import re

with open("index.html", "r") as f:
    html = f.read()

def add_poster(match):
    video_tag = match.group(0)
    src_match = re.search(r'src="([^"]+)"', video_tag)
    if not src_match:
        return video_tag
    src = src_match.group(1)
    if src.startswith("camera/") and src.endswith(".mp4"):
        poster_src = src[:-4] + ".jpg"
        if 'poster="' not in video_tag:
            video_tag = video_tag.replace(f'src="{src}"', f'poster="{poster_src}" src="{src}"')
            
    video_tag = video_tag.replace('preload="none"', 'preload="metadata"')
    return video_tag

html = re.sub(r'<video[^>]+>', add_poster, html)

hover_script = """
        videos.forEach(video => {
            // Hover to preload for instant playback
            const parent = video.parentElement;
            parent.addEventListener('mouseenter', () => {
                if (video.preload !== 'auto') {
                    video.preload = 'auto';
                }
            });
"""

html = html.replace('videos.forEach(video => {', hover_script)

with open("index.html", "w") as f:
    f.write(html)
