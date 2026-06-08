import re
import os

html_content = open("index.html").read()

# 1. Update title and meta
html_content = re.sub(
    r'<title>Kling-Avatar</title>',
    r'<title>OmniDirector: Equipping Video Generation Models with Camera Control through General and Scalable Visual Representation</title>',
    html_content
)

html_content = re.sub(
    r'<meta name="description" content="Kling-Avatar:Grounding Multimodal Instructions for Cascaded\s*Long-Duration Avatar Animation Synthesis">',
    r'<meta name="description" content="OmniDirector: Equipping Video Generation Models with Camera Control through General and Scalable Visual Representation">',
    html_content
)

# 2. Update h2 title
html_content = re.sub(
    r'<h2 style="font-size: 3.2rem; font-weight: 400;  color: #f7fcf9;  ">\s*Kling-Avatar: Grounding Multimodal Instructions for Cascaded\s*Long-Duration Avatar Animation Synthesis\s*</h2>',
    r'<h2 style="font-size: 3.2rem; font-weight: 400;  color: #f7fcf9;  ">\n                OmniDirector: Equipping Video Generation Models with Camera Control through General and Scalable Visual Representation\n            </h2>',
    html_content
)

# 3. Update authors
authors_html = """            <span style="opacity: 0.6; font-size: 1.35rem;">
                <a>Jiwen Liu</a>,
                <a>Yan Zhou</a>,
                <a>Xiaohan Li</a>,
                <a>Zhixue Fang</a>,
                <a>Zhimin Zhang</a>,
                <a>Shujuan Li</a>,
                <a>Zijie Meng</a>
            </span>"""

html_content = re.sub(
    r'<span style="opacity: 0\.6; font-size: 1\.35rem;">\s*<a href="https://yikang98\.github\.io/".*?</span>',
    authors_html,
    html_content,
    flags=re.DOTALL
)

# The second span block
html_content = re.sub(
    r'<span style="opacity: 0\.6; font-size: 1\.35rem;">\s*<!-- <a href="https://yikang98\.github\.io/".*?</span>',
    '',
    html_content,
    flags=re.DOTALL
)

html_content = re.sub(r'<p></p>', '', html_content)
html_content = re.sub(r'<a style="opacity: 0.6; font-size: 1.3rem;"><sup>\*</sup>Equal contribution\s*<div style="margin-top: 20px;"></div>', '<div style="margin-top: 20px;"></div>', html_content)
html_content = re.sub(r'<span style="opacity: 0.6;">\s*<a style="font-size: 1.5rem; display: inline-block;">Kling Team, Kuaishou Technology</a>\s*</span>', '', html_content)

# 4. Update BibTeX
bibtex_old = r"""@article{ding2025kling-avatar,
  title={Kling-Avatar: Grounding Multimodal Instructions for Cascaded Long-Duration Avatar Animation Synthesis},
  author={Ding, Yikang and Liu, Jiwen and Zhang, Wenyuan and Wang, Zekun and Hu, Wentao and Cui, Liyuan and Lao, Mingming and Shao, Yingchao and Liu, Hui and Li, Xiaohan and Chen, Ming and Liu, Xiaoqiang and Liu, Yu-shen and Wan, Pengfei},
  journal={arXiv preprint arXiv:2509.09595},
  year={2025}
}"""

bibtex_new = """@article{liu2025omnidirector,
  title={OmniDirector: Equipping Video Generation Models with Camera Control through General and Scalable Visual Representation},
  author={Liu, Jiwen and Zhou, Yan and Li, Xiaohan and Fang, Zhixue and Zhang, Zhimin and Li, Shujuan and Meng, Zijie},
  journal={arXiv preprint},
  year={2026}
}"""
html_content = html_content.replace(bibtex_old, bibtex_new)

# 5. Generate sections
sections = [
    ("Scene Generalization", "scene_generalization"),
    ("Multi Shot", "multi_shot"),
    ("Dynamic Motion", "dynamic_motion"),
    ("Special Camera Movement", "special_camera_movement")
]

sections_html = ""
for title, folder in sections:
    sections_html += f'    <section id="{title.replace(" ", "-")}">\n'
    sections_html += f'        <div class="title">{title}</div>\n'
    sections_html += '        <div class="masonry">\n'
    
    files = [f for f in os.listdir(f"camera/{folder}") if f.endswith(".mp4")]
    for f in sorted(files):
        sections_html += f'            <div class="prompt-wrap audio-control">\n'
        sections_html += f'                <video playsinline controls loop preload="none" src="camera/{folder}/{f}"></video>\n'
        sections_html += f'            </div>\n'
        
    sections_html += '        </div>\n'
    sections_html += '    </section>\n\n'

# Find where to replace videos.
# The videos start from <section id="High-Quality Videos with Accurate Lip–Audio Alignment" style="margin-top: 200px;">
# And end before <section id="Pipeline">

start_idx = html_content.find('<section id="High-Quality Videos with Accurate Lip–Audio Alignment"')
end_idx = html_content.find('<section id="Pipeline">')

if start_idx != -1 and end_idx != -1:
    html_content = html_content[:start_idx] + sections_html + "    " + html_content[end_idx:]

with open("index.html", "w") as f:
    f.write(html_content)

print("Done")
