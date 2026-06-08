import re
import urllib.parse

with open("index.html", "r") as f:
    html = f.read()

def encode_paths(match):
    video_tag = match.group(0)
    
    # Extract src
    src_match = re.search(r'src="([^"]+)"', video_tag)
    if not src_match:
        return video_tag
    src = src_match.group(1)
    
    # Extract poster
    poster_match = re.search(r'poster="([^"]+)"', video_tag)
    
    # URL encode the paths (but keep the slashes)
    if src.startswith("camera/"):
        encoded_src = urllib.parse.quote(urllib.parse.unquote(src))
        video_tag = video_tag.replace(f'src="{src}"', f'src="{encoded_src}"')
        
    if poster_match:
        poster = poster_match.group(1)
        if poster.startswith("camera/"):
            encoded_poster = urllib.parse.quote(urllib.parse.unquote(poster))
            video_tag = video_tag.replace(f'poster="{poster}"', f'poster="{encoded_poster}"')
            
    # Change preload="metadata" or preload="auto" to preload="none"
    video_tag = re.sub(r'preload="(metadata|auto)"', 'preload="none"', video_tag)
    
    return video_tag

html = re.sub(r'<video[^>]+>', encode_paths, html)

with open("index.html", "w") as f:
    f.write(html)
