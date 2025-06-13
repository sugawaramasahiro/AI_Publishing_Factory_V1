from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import os, time

def upload_to_kdp(title):
    try:
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")

        # ★ Service に渡す
        service = Service(ChromeDriverManager().install())
        driver  = webdriver.Chrome(service=service, options=options)

        driver.get("https://kdp.amazon.co.jp/")
        input("🔐 KDPへログインしたら Enter → ")

        wait = WebDriverWait(driver, 20)
        wait.until(EC.element_to_be_clickable((By.LINK_TEXT,"電子書籍または有料本を作成"))).click()

        wait.until(EC.presence_of_element_located((By.ID,"bookTitle"))).send_keys(title)
        driver.find_element(By.ID,"authorName").send_keys("MP")
        driver.find_element(By.ID,"bookUpload").send_keys(os.path.abspath("output/book.txt"))

        # 表紙
        wait.until(EC.element_to_be_clickable((By.ID,"coverUploadOption"))).click()
        file_input = wait.until(EC.presence_of_element_located(
            (By.XPATH,"//input[@type='file' and contains(@accept,'image')]")))
        driver.execute_script("arguments[0].style.display='block';", file_input)
        file_input.send_keys(os.path.abspath("assets/cover_sample.jpg"))

        driver.find_element(By.ID,"saveAndContinue").click()
        time.sleep(5)
        driver.quit()
        return True

    except Exception as e:
        print(f"⚠️ Selenium エラー: {e}")
        return False
