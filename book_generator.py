import os
from docx import Document
from ebooklib import epub

# ファイルパス
docx_path = "ロードバイク30km本_完成版.docx"
cover_path = "assets/cover_sample.jpg"
output_epub = "book.epub"

# Word読み込み
doc = Document(docx_path)
book = epub.EpubBook()
book.set_identifier("roadbike-30km")
book.set_title("ロードバイク初心者が30km/h巡航する方法")
book.set_language("ja")
book.add_author("ＭＰ")

# 表紙
if os.path.exists(cover_path):
    with open(cover_path, "rb") as f:
        book.set_cover("cover.jpg", f.read())

# 本文パース
chapters = []
current_title = "はじめに"
current_content = ""

for para in doc.paragraphs:
    text = para.text.strip()
    if not text:
        continue
    if text.startswith("第") and "章" in text:
        if current_content:
            html = f"<h1>{current_title}</h1><p>{current_content.replace(chr(10), '<br/>')}</p>"
            c = epub.EpubHtml(title=current_title, file_name=f"{current_title}.xhtml", lang="ja")
            c.content = html
            book.add_item(c)
            chapters.append(c)
        current_title = text
        current_content = ""
    else:
        current_content += text + "\n"

# 最後の章
if current_content:
    html = f"<h1>{current_title}</h1><p>{current_content.replace(chr(10), '<br/>')}</p>"
    c = epub.EpubHtml(title=current_title, file_name=f"{current_title}.xhtml", lang="ja")
    c.content = html
    book.add_item(c)
    chapters.append(c)

book.toc = chapters
book.add_item(epub.EpubNcx())
book.add_item(epub.EpubNav())

style = epub.EpubItem(uid="style_nav", file_name="style/nav.css", media_type="text/css",
                      content='BODY { font-family: sans-serif; }')
book.add_item(style)

epub.write_epub(output_epub, book)
print("✅ EPUB書き出し成功！ →", output_epub)
