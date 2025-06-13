from docx import Document
from ebooklib import epub
import os, pathlib

proj        = r"C:\AI_Publishing_Factory_V1"
docx_path   = os.path.join(proj, "ロードバイク30km本_完成版.docx")
cover_path  = os.path.join(proj, "assets", "cover_sample.jpg")
output_epub = os.path.join(proj, "book.epub")

doc  = Document(docx_path)
book = epub.EpubBook()
book.set_identifier("roadbike-30km")
book.set_title("ロードバイク初心者が30km/h巡航する方法")
book.set_language("ja")
book.add_author("ＭＰ")

# 表紙
if os.path.exists(cover_path):
    with open(cover_path,"rb") as f:
        book.set_cover("cover.jpg", f.read())

chapters, cur_title, cur_body = [], "はじめに", ""
for p in doc.paragraphs:
    txt = p.text.strip()
    if not txt: continue
    if txt.startswith("第") and "章" in txt:
        if cur_body:
            html = f"<h1>{cur_title}</h1><p>{cur_body.replace(chr(10),'<br/>')}</p>"
            sec  = epub.EpubHtml(title=cur_title, file_name=f"{cur_title}.xhtml", lang="ja")
            sec.content = html; book.add_item(sec); chapters.append(sec)
        cur_title, cur_body = txt, ""
    else:
        cur_body += txt + "\\n"

if cur_body:
    html = f"<h1>{cur_title}</h1><p>{cur_body.replace(chr(10),'<br/>')}</p>"
    sec  = epub.EpubHtml(title=cur_title, file_name=f"{cur_title}.xhtml", lang="ja")
    sec.content = html; book.add_item(sec); chapters.append(sec)

book.toc = chapters
book.add_item(epub.EpubNcx()); book.add_item(epub.EpubNav())
book.add_item(epub.EpubItem(uid="style",file_name="style.css",
            media_type="text/css",content="body{font-family:sans-serif;}"))

epub.write_epub(output_epub, book)
print("✅ EPUB 書き出し成功！ →", output_epub)
