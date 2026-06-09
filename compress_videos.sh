#!/bin/bash
find camera -name "*.mp4" | while read file; do
    echo "Compressing $file..."
    ffmpeg -y -i "$file" -vcodec libx264 -vf scale=800:-2 -crf 28 -preset fast -c:a copy -movflags +faststart "${file}.tmp.mp4" -loglevel error </dev/null
    if [ $? -eq 0 ]; then
        mv "${file}.tmp.mp4" "$file"
        base="${file%.mp4}"
        ffmpeg -y -i "$file" -vframes 1 -q:v 2 "${base}.jpg" -loglevel error </dev/null
    fi
done
echo "All videos compressed!"
