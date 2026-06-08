import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Fix the hover css
html = html.replace('.prompt-wrap:hover_disabled video::-webkit-media-controls', '.prompt-wrap:hover video::-webkit-media-controls')

# Find all masonry blocks
masonry_pattern = re.compile(r'<div class="masonry">(.*?)</div>\s*</section>', re.DOTALL)

def replace_masonry(match):
    inner_content = match.group(1)
    
    # Extract all prompt-wrap blocks
    wrap_pattern = re.compile(r'<div class="prompt-wrap audio-control">.*?</div>', re.DOTALL)
    wraps = wrap_pattern.findall(inner_content)
    
    col1 = []
    col2 = []
    col3 = []
    
    for i, wrap in enumerate(wraps):
        if i % 3 == 0:
            col1.append(wrap)
        elif i % 3 == 1:
            col2.append(wrap)
        else:
            col3.append(wrap)
            
    res = '<div class="container">\n'
    
    res += '            <div class="column col1">\n'
    for w in col1:
        res += '                ' + w + '\n'
    res += '            </div>\n'
    
    res += '            <div class="column col2">\n'
    for w in col2:
        res += '                ' + w + '\n'
    res += '            </div>\n'
    
    res += '            <div class="column col3">\n'
    for w in col3:
        res += '                ' + w + '\n'
    res += '            </div>\n'
    
    res += '        </div>\n    </section>'
    
    return res

new_html = masonry_pattern.sub(replace_masonry, html)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(new_html)
