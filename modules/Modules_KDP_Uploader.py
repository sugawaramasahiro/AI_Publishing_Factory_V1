from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time

def upload_to_kdp(title, author, filepath, cover_path):
    options = Options()
    options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=options)

    # KDP ログイン
    driver.get("https://kdp.amazon.co.jp/")
    print("🔑 手動でログインしてください（2段階認証があるため）")
    input("✅ ログインが完了したら Enter を押してください：")

    # 本棚追加ページへ
    driver.get("https://kdp.amazon.co.jp/ja_JP/title-setup/")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    time.sleep(3)

    # タイトル・著者名
    try:
        title_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "title"))
        )
        title_input.send_keys(title)

        author_input = driver.find_element(By.ID, "author")
        author_input.send_keys(author)
        print("✍️ タイトル・著者を自動入力しました")
    except Exception as e:
        print("❌ タイトル・著者の自動入力に失敗しました:", e)

    # 原稿ファイルのアップロード
    try:
        manuscript_upload = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='file'][accept='.doc,.docx,.epub']"))
        )
        manuscript_upload.send_keys(os.path.abspath(filepath))
        print(f"📄 原稿ファイルをアップロード：{filepath}")
    except Exception as e:
        print("❌ 原稿アップロード失敗:", e)

    # 表紙ファイルのアップロード
    try:
        cover_upload = driver.find_element(By.CSS_SELECTOR, "input[type='file'][accept='.jpg,.jpeg,.png,.tif,.tiff']")
        cover_upload.send_keys(os.path.abspath(cover_path))
        print(f"🖼️ 表紙ファイルをアップロード：{cover_path}")
    except Exception as e:
        print("❌ 表紙アップロード失敗:", e)

    # 「保存して次へ」クリック
    try:
        next_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@value='保存して次へ']"))
        )
        next_button.click()
        print("✅ 保存して次へ をクリックしました")
    except Exception as e:
        print("❌ 次へクリック失敗:", e)

    print("📦 KDP提出処理 完了！")

if __name__ == "__main__":
    upload_to_kdp(
        "AI出版入門",
        "山田太郎",
        "output/AI出版入門.epub",
        "output/AI出版入門_cover.png"
    )
