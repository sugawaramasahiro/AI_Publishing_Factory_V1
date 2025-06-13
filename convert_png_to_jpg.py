from PIL import Image
import os

source_path = "assets/cover_sample.png"
target_path = "assets/cover_sample.jpg"

if os.path.exists(source_path):
    img = Image.open(source_path).convert("RGB")
    img.save(target_path, "JPEG")
    print("✅ PNG→JPG変換 完了！")
else:
    print("❌ PNGファイルが見つかりません")
