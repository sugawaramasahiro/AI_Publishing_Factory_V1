import csv
from Modules_Cover_Generator import generate_cover
from Modules_Word_Exporter import export_to_word
from Modules_PDF_Exporter import export_to_pdf
from Modules_EPUB_Exporter import export_to_epub
from Modules_KDP_Packager import create_kdp_package
from ai_writer import WritingModule

def bulk_generate_books(csv_path="books.csv"):
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            title = row["title"]
            author = row["author"]
            genre = row["genre"]
            chapters = row["chapters"].split("\\n")

            print(f"📘 生成開始：{title}")

            full_chapters = {}
            for chapter in chapters:
                content = WritingModule().generate_chapter(chapter, genre)
                full_chapters[chapter] = content

            generate_cover(title, author, genre)
            export_to_word(title, author, full_chapters)
            export_to_pdf(title, author, full_chapters)
            export_to_epub(title, author, "\\n".join(full_chapters.values()))
            create_kdp_package(title, author, genre)

            print(f"✅ 完了：{title}\\n")

if __name__ == "__main__":
    bulk_generate_books()
