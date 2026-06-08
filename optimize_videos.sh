#!/bin/bash
find camera -name "*.mp4" | while read file; do
    base="${file%.mp4}"
    echo "Processing $file..."
    # 1. Extract poster
    if [ ! -f "${base}.jpg" ]; then
        ffmpeg -y -i "$file" -vframes 1 -q:v 2 "${base}.jpg" -loglevel error </dev/null
    fi
    # 2. Add faststart
    ffmpeg -y -i "$file" -c copy -movflags +faststart "${base}_tmp.mp4" -loglevel error </dev/null
    if [ $? -eq 0 ]; then
        mv "${base}_tmp.mp4" "$file"
    fi
done
echo "All done!"