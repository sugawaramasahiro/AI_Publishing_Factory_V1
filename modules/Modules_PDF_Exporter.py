from fpdf import FPDF
import os

def export_to_pdf(title, author, chapters_dict):
    pdf = FPDF()
    pdf.add_page()

    # フォントフォルダのパス
    font_dir = os.path.join(os.path.dirname(__file__), "..", "fonts")
    font_path = os.path.join(font_dir, "NotoSansJP-Regular.otf")

    try:
        # Unicodeフォントを追加
        pdf.add_font("NotoSansJP", "", font_path, uni=True)
        pdf.set_font("NotoSansJP", size=24)
        pdf.cell(200, 10, txt=title, ln=True, align="C")

        pdf.set_font("NotoSansJP", size=14)
        pdf.cell(200, 10, txt=f"著者：{author}", ln=True, align="C")
        pdf.ln(10)

        for chapter_title, chapter_content in chapters_dict.items():
            pdf.add_page()
            pdf.set_font("NotoSansJP", size=16)
            pdf.cell(200, 10, txt=chapter_title, ln=True, align="L")
            pdf.ln(10)
            pdf.set_font("NotoSansJP", size=12)
            pdf.multi_cell(0, 8, txt=chapter_content.strip())
            pdf.ln(5)

        os.makedirs("output", exist_ok=True)
        pdf.output(f"output/{title}.pdf")
        print(f"✅ PDFを書き出しました：output/{title}.pdf")

    except Exception as e:
        print(f"❌ PDF作成中にエラーが発生しました: {e}")
