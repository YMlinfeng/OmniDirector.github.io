find /Users/mengzijie/Downloads/project/KlingCameraControl.github.io/camera \
  -type f \( -iname "*.jpg" -o -iname "*.jpeg" -o -iname "*.png" \) | \
while IFS= read -r f; do
  cwebp -q 80 "$f" -o "${f%.*}.webp"
done

# find /Users/mengzijie/Downloads/project/KlingCameraControl.github.io/camera \
#   -type f \( -iname "*.jpg" -o -iname "*.jpeg" -o -iname "*.png" \) -delete

