#!/bin/bash

# ===== 配置区 =====
BASE_DIR="/Users/mengzijie/Downloads/project/KlingCameraControl.github.io/camera"
SUFFIX="_labeled"                                   # 保存时追加的后缀
FONT="/System/Library/Fonts/Supplemental/Arial.ttf" # Mac 自带字体

# 文字样式（位置和大小都用分辨率比例表示，保证同分辨率的图/视频一致）
FONTSIZE="h/20"          # 字号 = 高度的 1/20
MARGIN_X="w/50"          # 左右边距
MARGIN_Y="h/40"          # 上边距

# 左上角 ref，右上角 generated（带半透明黑底，方便看清）
VF="drawtext=fontfile=${FONT}:text='reference':fontcolor=white:fontsize=${FONTSIZE}:box=1:boxcolor=black@0.5:boxborderw=8:x=${MARGIN_X}:y=${MARGIN_Y}, \
drawtext=fontfile=${FONT}:text='generation':fontcolor=white:fontsize=${FONTSIZE}:box=1:boxcolor=black@0.5:boxborderw=8:x=w-tw-${MARGIN_X}:y=${MARGIN_Y}"

# ===== 处理图片 =====
find "$BASE_DIR" -type f \( -iname "*.jpg" -o -iname "*.jpeg" -o -iname "*.png" \) | while read -r file; do
    dir=$(dirname "$file"); base=$(basename "$file")
    name="${base%.*}"; ext="${base##*.}"
    [[ "$name" == *"$SUFFIX" ]] && continue          # 跳过已处理的
    out="$dir/${name}${SUFFIX}.${ext}"
    echo "图片: $file"
    ffmpeg -y -loglevel error -i "$file" -vf "$VF" "$out"
done

# ===== 处理视频 =====
find "$BASE_DIR" -type f \( -iname "*.mp4" -o -iname "*.mov" -o -iname "*.avi" -o -iname "*.mkv" -o -iname "*.webm" \) | while read -r file; do
    dir=$(dirname "$file"); base=$(basename "$file")
    name="${base%.*}"; ext="${base##*.}"
    [[ "$name" == *"$SUFFIX" ]] && continue
    out="$dir/${name}${SUFFIX}.${ext}"
    echo "视频: $file"
    # 保留原音频，重新编码视频
    ffmpeg -y -loglevel error -i "$file" -vf "$VF" -c:a copy "$out"
done

echo "全部完成！"

