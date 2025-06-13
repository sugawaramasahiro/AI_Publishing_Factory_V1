import requests
import os

# Canva APIの事前設定
CANVA_API_KEY = "あなたのAPIキー"
TEMPLATE_ID = "あなたのテンプレートID"   # CanvaテンプレのID
TITLE = "あなたの本のタイトル"           # ダイナミックに渡してもOK

# 1. テンプレに値を流し込んで画像生成
def generate_canva_cover():
    url = f"https://api.canva.com/v1/designs/{TEMPLATE_ID}/export"
    headers = {"Authorization": f"Bearer {CANVA_API_KEY}"}
    params = {
        "format": "jpg",
        "title": TITLE,
        # 他に必要なカスタムパラメータは公式API参照
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        os.makedirs("output", exist_ok=True)
        with open("output/cover.jpg", "wb") as f:
            f.write(response.content)
        print("✅ Canva自動表紙ダウンロード完了！")
    else:
        print("❌ Canva APIエラー", response.status_code, response.text)

if __name__ == "__main__":
    generate_canva_cover()
