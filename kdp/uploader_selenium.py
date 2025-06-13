from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import os

def upload_to_kdp(title="ロードバイク30km本_完成版", author="MP"):
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    # 1. KDPログインページを開く
    driver.get("https://kdp.amazon.co.jp/ja_JP/")
    print("KDPにアクセスしました。手動でログインしてください（自動化は規約注意）")

    # 2. 手動ログインを待つ（例：90秒間待機）
    time.sleep(90)

    # 3. 「本棚」→「本を追加」ボタンを探す
    try:
        add_button = driver.find_element(By.LINK_TEXT, "本を追加")
        add_button.click()
        print("本棚を追加ボタンをクリックしました。")
    except Exception as e:
        print("本棚を追加ボタンが見つかりません。UI変更時はここを修正:", e)

    time.sleep(5)

    # 4. タイトル・著者自動入力（ID等は実際の画面で確認し調整必要）
    try:
        driver.find_element(By.ID, "book-title-textbox").send_keys(title)
        driver.find_element(By.ID, "author-textbox").send_keys(author)
        print("タイトル・著者を自動入力しました。")
    except Exception as e:
        print("タイトル・著者入力欄が見つからない場合、手動で入力してください。", e)

    # 5. 原稿（manuscript.docx）アップロード
    try:
        manuscript_path = os.path.abspath("output/manuscript.docx")
        upload_inputs = driver.find_elements(By.CSS_SELECTOR, "input[type='file']")
        if upload_inputs:
            upload_inputs[0].send_keys(manuscript_path)
            print("原稿ファイルをアップロードしました。")
        else:
            print("原稿アップロード用のinputタグが見つかりません。")
    except Exception as e:
        print("原稿アップロードに失敗しました。手動でアップロードしてください。", e)

    time.sleep(5)

    # 6. 表紙（cover.jpg）アップロード
    try:
        cover_path = os.path.abspath("output/cover.jpg")
        upload_inputs = driver.find_elements(By.CSS_SELECTOR, "input[type='file']")
        if len(upload_inputs) > 1:
            upload_inputs[1].send_keys(cover_path)
            print("表紙ファイルをアップロードしました。")
        else:
            print("表紙アップロード用のinputタグが見つかりません。")
    except Exception as e:
        print("表紙アップロードに失敗しました。手動でアップロードしてください。", e)

    print("✅ KDP提出処理が完了しました。続きは手動で進めてください。")
    # driver.quit()

if __name__ == "__main__":
    upload_to_kdp()
