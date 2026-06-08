import os
from PIL import Image

def is_black(image_path):
    try:
        img = Image.open(image_path)
        extrema = img.convert("L").getextrema()
        if extrema == (0, 0):
            return True
        return False
    except Exception as e:
        print(f"Error reading {image_path}: {e}")
        return False

folder = "camera/scene_generalization"
files = [f for f in os.listdir(folder) if f.endswith(".jpg")]
black_count = 0
for f in files:
    if is_black(os.path.join(folder, f)):
        black_count += 1

print(f"Total JPGs: {len(files)}, Black JPGs: {black_count}")
