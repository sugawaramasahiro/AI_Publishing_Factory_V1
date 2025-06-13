from PIL import Image
import os

def make_white_cover():
    width, height = 2560, 1600
    img = Image.new("RGB", (width, height), (255, 255, 255))
    os.makedirs("output", exist_ok=True)
    img.save("output/cover.jpg")
    print("✅ cover.jpg (白紙カバー) 作成完了！")

if __name__ == "__main__":
    make_white_cover()
