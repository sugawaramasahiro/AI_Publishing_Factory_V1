import streamlit as st
from modules.kdp_upload import upload_to_kdp
from modules.ai_writer import generate_book
from modules.mail_sender import send_mail

st.set_page_config(page_title="AI出版所 V6", layout="centered")

with st.container():
    st.markdown("""
        <style>
        .main {
            background-color: #f5f5f5;
            padding: 2rem;
            border-radius: 12px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.05);
            max-width: 700px;
            margin: auto;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="main">', unsafe_allow_html=True)
    st.title("📘 AI出版所 V6 Integrated ダッシュボード")

    with st.form("book_form"):
        genre = st.selectbox("ジャンルを選んでください", ["睡眠", "ロードバイク", "恋愛", "ビジネス", "ファンタジー"])
        title = st.text_input("タイトルを入力")
        author = st.text_input("著者名を入力", value="MP")
        email = st.text_input("完成通知を送るメールアドレス")
        submit = st.form_submit_button("📘 電子書籍を生成する")

    if submit:
        with st.spinner("⏳ 電子書籍を生成中..."):
            content = generate_book(genre, title, author)
            with open("output/book.txt", "w", encoding="utf-8") as f:
                f.write(content)

            st.success("✅ 電子書籍が生成されました！")
            st.markdown("### 📖 生成された本文")
            st.text_area("出力結果", value=content, height=300)

            if upload_to_kdp(title):
                st.success("📤 KDPにアップロードされました！")

            if email:
                send_mail(email, title)
                st.success("✉️ メール通知を送信しました！")

    st.markdown("</div>", unsafe_allow_html=True)
