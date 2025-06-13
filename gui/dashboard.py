import streamlit as st
import os

def generate_canva_cover():
    # ここは上記 canva_cover_gen.py の中身をそのまま貼り付けてOK
    os.system("python canva_cover_gen.py")
    st.success("✅ Canva自動表紙生成・保存完了！")

st.set_page_config(page_title="AI出版所 V100", layout="wide")
st.title("🚀 Canva自動表紙生成ダッシュボード")

if st.button("🎨 Canvaで自動表紙を作成して保存"):
    generate_canva_cover()

# 必要に応じてバナー生成もボタン化可能
if st.button("📢 Canvaでバナー自動量産"):
    os.system("python canva_banner_gen.py")
    st.success("✅ Canvaバナー自動生成・保存完了！")
