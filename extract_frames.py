import os
import subprocess

src_dir = "/Users/mengzijie/Downloads/project/KlingCameraControl.github.io/camera/compare"
dst_dir = "/Users/mengzijie/Downloads/project/KlingCameraControl.github.io/image"

video_exts = {".mp4", ".mov", ".avi", ".mkv", ".flv", ".wmv", ".m4v", ".webm"}

os.makedirs(dst_dir, exist_ok=True)

count = 0
for filename in os.listdir(src_dir):
    name, ext = os.path.splitext(filename)
    if ext.lower() not in video_exts:
        continue

    video_path = os.path.join(src_dir, filename)
    out_path = os.path.join(dst_dir, name + ".jpg")

    # -frames:v 1 只取第一帧；-y 覆盖已存在文件
    cmd = [
        "ffmpeg", "-y",
        "-i", video_path,
        "-frames:v", "1",
        "-q:v", "2",
        out_path
    ]
    result = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if result.returncode == 0:
        print(f"✅ 已提取首帧: {filename} -> {name}.jpg")
        count += 1
    else:
        print(f"⚠️ 处理失败: {filename}")

print(f"\n完成！共处理 {count} 个视频。")