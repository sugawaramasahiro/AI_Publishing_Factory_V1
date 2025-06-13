from ebooklib import epub

def generate_epub(title, author, text, output_path):
    book = epub.EpubBook()
    book.set_identifier("id123456")
    book.set_title(title)
    book.set_language("en")
    book.add_author(author)

    c1 = epub.EpubHtml(title="Chapter 1", file_name="chap_01.xhtml", lang="en")
    c1.content = f"<h1>Chapter 1</h1><p>{text}</p>"

    book.add_item(c1)
    book.toc = (epub.Link("chap_01.xhtml", "Chapter 1", "chap_1"),)
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())

    book.spine = ["nav", c1]
    epub.write_epub(output_path, book)
    print("✅ EPUB生成完了")

if __name__ == "__main__":
    generate_epub("AI Publishing Sample", "MP", "これは自動生成されたEPUBです。", "output.epub")
