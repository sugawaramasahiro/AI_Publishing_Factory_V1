# main_local_pipeline.ps1

# 1. Word原稿を自動生成
Write-Host "▶ Word原稿を生成しています..."
python convert/word_generator.py

# 2. EPUBへ変換
Write-Host "▶ EPUBに変換しています..."
pandoc output/local_demo.docx -o output/local_demo.epub

# 3. 表紙画像自動生成
Write-Host "▶ カバー画像を生成しています..."
python convert/cover_generator.py

# 4. Streamlitダッシュボードを起動
Write-Host "▶ ダッシュボードを起動しています..."
Start-Process streamlit run gui/dashboard.py

# 5. （任意）KDP提出自動化
# Write-Host "▶ KDP自動アップロードを開始..."
# python kdp/uploader_selenium.py
