# convert/epub_converter.py

import subprocess
import os

def convert_to_epub(title):
    """
    Wordファイル（.docx）をEPUBファイルに変換する。
    Pandocがインストールされている必要があります。
    """
    input_path = f"output/{title}.docx"
    output_path = f"output/{title}.epub"

    # pandocコマンドで変換実行
    try:
        subprocess.run([
            "pandoc",
            input_path,
            "-o",
            output_path
        ], check=True)
        print(f"✅ EPUBファイルに変換完了: {output_path}")
    except subprocess.CalledProcessError:
        print("❌ EPUB変換に失敗しました。pandocが正しくインストールされているか確認してください。")
