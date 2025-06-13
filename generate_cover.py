from PIL import Image, ImageDraw

# サイズと背景色（青系）
img = Image.new("RGB", (600, 800), color=(70, 130, 180))
draw = ImageDraw.Draw(img)

# テキストを中央付近に配置
text = "Cover Sample"
text_position = (150, 380)
draw.text(text_position, text, fill=(255, 255, 255))

# 保存
img.save("assets/cover_sample.jpg")
print("✅ 仮のカバー画像を作成しました！")
