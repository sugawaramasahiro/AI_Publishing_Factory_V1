from ebooklib import epub

def create_epub(title, author, content, cover_path, output_path):
    book = epub.EpubBook()
    book.set_identifier("id123456")
    book.set_title(title)
    book.set_language("ja")
    book.add_author(author)

    if cover_path:
        book.set_cover("cover.jpg", open(cover_path, "rb").read())

    chapter = epub.EpubHtml(title="本文", file_name="chap_01.xhtml", lang="ja")
    chapter.content = f"<h1>{title}</h1><p>{content}</p>"
    book.add_item(chapter)

    book.toc = (epub.Link("chap_01.xhtml", "本文", "chap_01"),)
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())

    style = "BODY { font-family: serif; }"
    nav_css = epub.EpubItem(uid="style_nav", file_name="style/nav.css", media_type="text/css", content=style)
    book.add_item(nav_css)

    book.spine = ["nav", chapter]
    epub.write_epub(output_path, book)
    print(f"✅ EPUBファイル出力完了: {output_path}")

if __name__ == "__main__":
    with open("./output/manuscript.txt", "r", encoding="utf-8") as f:
        content = f.read()

    create_epub(
        title="サンプル電子書籍",
        author="MPさん",
        content=content,
        cover_path="./output/cover.jpg",
        output_path="./output/book.epub"
    )
