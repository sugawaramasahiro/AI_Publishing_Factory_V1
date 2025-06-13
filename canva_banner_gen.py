import requests
import os

CANVA_API_KEY = "あなたのAPIキー"
BANNER_TEMPLATE_ID = "あなたのバナーテンプレID"
BANNER_TITLE = "Campaign"  # 英語テスト値で実行推奨

def generate_canva_banner():
    url = f"https://api.canva.com/v1/designs/{BANNER_TEMPLATE_ID}/export"
    headers = {"Authorization": f"Bearer {CANVA_API_KEY}"}
    params = {
        "format": "jpg",
        "title": BANNER_TITLE
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        os.makedirs("output", exist_ok=True)
        fname = f"output/banner_{BANNER_TITLE}.jpg"
        with open(fname, "wb") as f:
            f.write(response.content)
        print("✅ Canvaバナー自動生成：", fname)
    else:
        print("❌ Canva APIエラー", response.status_code, response.text)

if __name__ == "__main__":
    generate_canva_banner()
