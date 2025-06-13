class WritingModule:
    def generate_text(self, genre, chapter_title, emotion):
        if emotion == "共感型":
            tone = "読者の悩みに寄り添って、共感できる文体で"
        elif emotion == "感動型":
            tone = "心に響くような感動的なストーリーで"
        elif emotion == "論理型":
            tone = "論理的で分かりやすく説明するように"
        elif emotion == "挑戦型":
            tone = "挑戦意欲をかきたてる熱い語り口で"
        elif emotion == "癒し型":
            tone = "やさしく、癒しのある語り口で"
        else:
            tone = "自然な文体で"

        prompt = f"{genre}の本の章「{chapter_title}」について、{tone}本文を500文字で書いてください。"
        result = f"📝 {tone}で書いた『{chapter_title}』の本文（ここにAI出力が入る）"
        return result
