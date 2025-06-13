
import streamlit as st
from modules.ai_writer import WritingModule
from modules.Modules_Cover_Generator import generate_cover
from modules.Modules_Cover_Mockup import mockup_3d
from modules.Modules_EPUB_Exporter import export_to_epub
from modules.Modules_Word_Exporter import export_to_word
from modules.Modules_PDF_Exporter import export_to_pdf
from modules.Modules_KDP_Packager import create_kdp_package
import pandas as pd
import os, subprocess, sys

# ─────────────────────────────────────────
# ページ設定 & 基本スタイル
# ─────────────────────────────────────────
st.set_page_config(page_title="AI Publishing Studio", page_icon="📘", layout="wide")
st.markdown('''<style>
body{font-family:"Segoe UI",sans-serif;}
div[data-testid="stSidebar"]{background:#fff;}
div[data-testid="stSidebar"] *{color:#111;}
input,textarea,select,div[role="combobox"],div[data-baseweb="select"] *{
  background:#fff;color:#111;opacity:1!important;border:1px solid #c8c8c8;}
button[kind]{background:#00BFFF;color:#fff;border:none;opacity:1;}
button[kind]:disabled{filter:grayscale(30%);}
</style>''', unsafe_allow_html=True)

# ─────────────────────────────────────────
# 自動チェック用ヘルパ
# ─────────────────────────────────────────
def mark_done(num: int):
    """チェックリスト項目 num(1始まり) を完了にする"""
    key = f"todo_{num-1}"
    st.session_state[key] = True

# ─────────────────────────────────────────
# サイドバー：メタデータ & ペルソナ
# ─────────────────────────────────────────
with st.sidebar:
    st.header("📑 メタデータ")
    title  = st.text_input("タイトル", "あなたの本のタイトル")
    author = st.text_input("著者名", "MP")                 # デフォルトを MP
    genre  = st.selectbox("ジャンル", ["ビジネス","小説","自己啓発",
                                      "技術書","ロードバイク","睡眠","その他"])
    st.header("👤 ペルソナ")
    age   = st.number_input("年齢", 10, 100, 30)
    pain  = st.text_input("悩み", "寝つきが悪い")
    goal  = st.text_input("理想", "朝スッキリ起きたい")
    if st.button("🔄 リセット"):
        st.session_state.clear()
        st.rerun()

# ログ用
def log_file(path:str):
    st.session_state.setdefault("files", []).append(path)

# ─────────────────────────────────────────
# タブ
# ─────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["🖋️ 本文", "🎨 表紙", "📤 出力", "📊 分析", "📋 チェック"])

# ===== TAB1 本文 =====
with tab1:
    st.subheader("🖋️ 本文生成")
    colL, colR = st.columns(2)

    # 複数章
    with colL:
        ch_text = st.text_area("章タイトル（改行区切り）",
                               "はじめに\n第1章\n第2章\nおわりに", height=240)
        if st.button("✒️ まとめて生成"):
            writer = WritingModule()
            st.session_state["chapters_dict"] = {
                c: writer.generate_chapter(c, genre, age, pain, goal)
                for c in ch_text.strip().split("\n")
            }
            st.success("複数章生成完了！")
            mark_done(5); mark_done(6)    # ⑤⑥

    # 単体章 + 感情
    with colR:
        ch_title = st.text_input("単体章タイトル", "第1章 基礎")
        emotion  = st.selectbox("感情トーン",
                                ["共感型","感動型","論理型","挑戦型","癒し型"])
        if st.button("📖 感情付き生成"):
            writer = WritingModule()
            txt = writer.generate_text(genre, ch_title, emotion, age, pain, goal)
            st.session_state["full_text"] = txt
            st.text_area("プレビュー", txt, height=240)

# ===== TAB2 表紙 =====
with tab2:
    st.subheader("🎨 表紙＆モックアップ")
    if st.button("🖼️ 表紙PNG生成"):
        p = generate_cover(title, author, genre, "共感型")
        st.session_state["cover_path"] = p
        st.image(p, caption="Flat Cover", use_container_width=True)
        log_file(p)
        mark_done(14)     # ⑭

    if st.button("📸 3Dモックアップ") and "cover_path" in st.session_state:
        mock = mockup_3d(st.session_state["cover_path"])
        st.image(mock, caption="3D Mockup", use_container_width=True)
        log_file(mock)

# ===== TAB3 出力 =====
with tab3:
    st.subheader("📤 ドキュメント出力")
    chapters = st.session_state.get("chapters_dict",
                 {"章": st.session_state.get("full_text", "")})

    col1, col2, col3, col4 = st.columns(4)
    if col1.button("Word"):
        p = export_to_word(title, author, chapters);  log_file(p); mark_done(12)
    if col2.button("PDF"):
        p = export_to_pdf(title, author, chapters);   log_file(p); mark_done(12)
    if col3.button("EPUB"):
        p = export_to_epub(title, author, "\n".join(chapters.values())); log_file(p)
    if col4.button("ZIP"):
        export_to_word(title, author, chapters)
        export_to_pdf(title, author, chapters)
        p = create_kdp_package(title, author, genre); log_file(p); st.toast("KDP ZIP 完了")

    # ── 🚀 ワンクリック出版 ─────────────────────
    st.markdown("---")
    if st.button("🚀 ワンクリック出版"):
        writer = WritingModule()

        # 章立てが無ければ AI に提案させる
        if "chapters_dict" not in st.session_state:
            auto_titles = writer.propose_outline(genre, goal)
            st.session_state["chapters_dict"] = {
                t: writer.generate_chapter(t, genre, age, pain, goal)
                for t in auto_titles}
            chapters = st.session_state["chapters_dict"]
            mark_done(4); mark_done(5); mark_done(6)

        # 表紙自動生成
        cov = generate_cover(title, author, genre, "共感型")
        mock = mockup_3d(cov)
        log_file(cov); log_file(mock); mark_done(14)

        # ドキュメント全部
        export_to_word(title, author, chapters);  mark_done(12)
        export_to_pdf(title, author, chapters);   mark_done(12)
        export_to_epub(title, author, "\n".join(chapters.values()))
        zp = create_kdp_package(title, author, genre); log_file(zp)

        st.toast("🎉 出版パッケージ完成！")

# ===== TAB4 分析 =====
with tab4:
    st.subheader("📊 感情ヒートマップ")
    if st.button("スコア計算") and "chapters_dict" in st.session_state:
        rows = [{"章": c, **WritingModule.classify_emotion(t)}
                for c, t in st.session_state["chapters_dict"].items()]
        pd.DataFrame(rows).set_index("章").pipe(st.bar_chart)

# ===== TAB5 チェックリスト =====
with tab5:
    st.subheader("📋 出版フロー・チェックリスト")
    todos = [
        '① 前準課題（事前にやっておく）',
        '② 出版予定日を決める',
        '③ コンセプトを決める',
        '④ 本の構成を考える',
        '⑤ 目次を考える',
        '⑥ 章立てに沿って本文を書く',
        '⑦ 後書きを書く',
        '⑧ 著者プロフィールを書く',
        '⑨ 参考文献一覧を付ける',
        '⑩ 奥付を付ける',
        '⑪ はじめに（前付け）を書く',
        '⑫ 本文＆スタイルをリライト',
        '⑬ 目次を最終調整する',
        '⑭ 表紙を作成する',
        '⑮ Kindle プレビュアーで原稿確認'
    ]
    for i, text in enumerate(todos):
        k = f"todo_{i}"
        if k not in st.session_state:
            st.session_state[k] = False
        st.checkbox(text, key=k)

    done = sum(st.session_state[f"todo_{i}"] for i in range(len(todos)))
    st.progress(done / len(todos))

# ───────── 生成ログ (サイドバー下) ─────────
with st.sidebar.expander("📂 生成ログ・ファイル一覧", expanded=True):
    if "full_text" in st.session_state:
        st.markdown("**📝 本文プレビュー**")
        st.text_area(" ", st.session_state["full_text"], height=150)
    if "files" in st.session_state:
        st.markdown("**📄 出力ファイル**")
        for p in st.session_state["files"]:
            st.write(f"✅ `{p}`")
        if st.button("📁 output フォルダを開く"):
            folder = os.path.abspath("output")
            if sys.platform.startswith("win"):
                subprocess.run(["explorer", folder])
            elif sys.platform.startswith("darwin"):
                subprocess.run(["open", folder])
            else:
                subprocess.run(["xdg-open", folder])
