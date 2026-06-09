# #!/bin/bash
# find camera -name "*.mp4" | while read file; do
#     base="${file%.mp4}"
#     echo "Processing $file..."
#     # 1. Extract poster
#     if [ ! -f "${base}.jpg" ]; then
#         ffmpeg -y -i "$file" -vframes 1 -q:v 2 "${base}.jpg" -loglevel error </dev/null
#     fi
#     # 2. Add faststart
#     ffmpeg -y -i "$file" -c copy -movflags +faststart "${base}_tmp.mp4" -loglevel error </dev/null
#     if [ $? -eq 0 ]; then
#         mv "${base}_tmp.mp4" "$file"
#     fi
# done
# echo "All done!"


#!/bin/bash

# ============================================================
# 可调参数区（按需修改下面的数值）
# ============================================================

# ---------- 首帧图片压缩参数 ----------
# IMG_QUALITY：JPG 画质，取值范围 1-31
#   数值越小画质越好、文件越大；数值越大压缩越狠、文件越小
#   常用范围：2（高画质）~ 8（明显压缩）。推荐 2-5
IMG_QUALITY=1

# IMG_SCALE：图片缩放宽度（像素）。-1 表示保持原始尺寸不缩放
#   例如设为 1280 则把图片等比缩放到宽 1280；高度自动按比例计算
#   想缩小文件可以降低这个值，比如 1280 / 960 / 640
IMG_SCALE=-1


# ---------- 视频压缩参数 ----------
# 是否对视频重新编码压缩：true = 压缩，false = 只做 faststart 不压缩（无损搬运）
VIDEO_COMPRESS=false

# 下面这几个参数在 VIDEO_COMPRESS=false 时不起作用，可以忽略
# VIDEO_CRF：视频画质，取值范围 0-51（H.264）
#   数值越小画质越好、文件越大；数值越大压缩越狠、文件越小
#   常用范围：18（视觉无损）~ 28（明显压缩）。推荐 23-28
#   注意：CRF 每 +6 文件大约减半，每 -6 文件大约翻倍
VIDEO_CRF=26

# VIDEO_PRESET：编码速度/压缩效率
#   可选：ultrafast superfast veryfast faster fast medium slow slower veryslow
#   越慢压缩效率越高（同画质文件更小），但耗时更长。推荐 medium 或 slow
VIDEO_PRESET=medium

# VIDEO_SCALE：视频缩放宽度（像素）。-1 表示保持原始尺寸不缩放
#   例如设为 1280 表示压到 720p 宽度。想减小文件可降低分辨率
VIDEO_SCALE=-1

# ============================================================
# 以下为执行逻辑，一般无需修改
# ============================================================

find camera -name "*.mp4" | while read file; do
    base="${file%.mp4}"
    echo "Processing $file..."

    # ---------- 1. 提取首帧并压缩成图片 ----------
    if [ ! -f "${base}.jpg" ]; then
        if [ "$IMG_SCALE" -eq -1 ]; then
            # 不缩放
            ffmpeg -y -i "$file" -vframes 1 -q:v "$IMG_QUALITY" \
                "${base}.jpg" -loglevel error </dev/null
        else
            # 等比缩放到指定宽度（-2 保证高度为偶数）
            ffmpeg -y -i "$file" -vframes 1 -q:v "$IMG_QUALITY" \
                -vf "scale=${IMG_SCALE}:-2" \
                "${base}.jpg" -loglevel error </dev/null
        fi
    fi

    # ---------- 2. 处理视频 ----------
    if [ "$VIDEO_COMPRESS" = true ]; then
        # 重新编码压缩视频
        if [ "$VIDEO_SCALE" -eq -1 ]; then
            ffmpeg -y -i "$file" \
                -c:v libx264 -crf "$VIDEO_CRF" -preset "$VIDEO_PRESET" \
                -c:a aac -b:a 128k \
                -movflags +faststart \
                "${base}_tmp.mp4" -loglevel error </dev/null
        else
            ffmpeg -y -i "$file" \
                -c:v libx264 -crf "$VIDEO_CRF" -preset "$VIDEO_PRESET" \
                -vf "scale=${VIDEO_SCALE}:-2" \
                -c:a aac -b:a 128k \
                -movflags +faststart \
                "${base}_tmp.mp4" -loglevel error </dev/null
        fi
    else
        # 不压缩，仅添加 faststart（无损搬运，适合网页快速播放）
        ffmpeg -y -i "$file" -c copy -movflags +faststart \
            "${base}_tmp.mp4" -loglevel error </dev/null
    fi

    # 替换原文件
    if [ $? -eq 0 ]; then
        mv "${base}_tmp.mp4" "$file"
    else
        echo "⚠️  Failed to process $file, keeping original."
        rm -f "${base}_tmp.mp4"
    fi
done

echo "All done!"