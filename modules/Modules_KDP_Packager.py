import os
import json
import zipfile

def create_kdp_package(title, author, genre, output_path="output"):
    docx_path = os.path.join(output_path, f"{title}.docx")
    cover_path = os.path.join(output_path, f"{title}_cover.png")
    metadata_path = os.path.join(output_path, f"{title}_metadata.json")
    zip_path = os.path.join(output_path, "kdp_package.zip")

    # メタ情報作成
    metadata = {
        "title": title,
        "author": author,
        "genre": genre
    }

    with open(metadata_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)

    # ZIP作成
    with zipfile.ZipFile(zip_path, "w") as zipf:
        for file in [docx_path, cover_path, metadata_path]:
            if os.path.exists(file):
                zipf.write(file, arcname=os.path.basename(file))
                print(f"✅ {os.path.basename(file)} をZIPに追加しました")
            else:
                print(f"⚠️ {file} が見つかりませんでした")

    print(f"📦 ZIPパッケージ作成完了：{zip_path}")
    return zip_path

# CLI用テスト
if __name__ == "__main__":
  create_kdp_package("ビジネス睡眠入門", "山田太郎", "ビジネス")

