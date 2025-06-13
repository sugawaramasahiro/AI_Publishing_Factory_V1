from __future__ import annotations
import os, openai, datetime, html

# ── OpenAI キー ──
openai.api_key = os.getenv("OPENAI_API_KEY")

class WritingModule:
    # 感情トーン辞書
    tone_dict = {
        "共感型": "読者の悩みに寄り添う",
        "感動型": "心に響く物語調で",
        "論理型": "論理的かつ分かりやすく",
        "挑戦型": "鼓舞する熱い語り口で",
        "癒し型": "やさしく癒やす語り口で",
    }

    # ─────────────────────────
    # 章ごとのサンプル本文生成
    # ─────────────────────────
    def generate_chapter(self, title: str, genre: str,
                         age: int, pain: str, goal: str) -> str:
        return (
            f"{age}歳の読者が『{pain}』で悩み『{goal}』を望む想定で、"
            f"章「{title}」を{genre}として解説します。"
        )

    # ─────────────────────────
    # 感情付き本文生成（GPT 呼び出し）
    # ─────────────────────────
    def generate_text(self, genre: str, title: str, emotion: str,
                      age: int, pain: str, goal: str) -> str:
        tone = self.tone_dict.get(emotion, "自然な文体で")
        prompt = (
            f"{age}歳読者の悩み『{pain}』を解決し『{goal}』を叶えるため、"
            f"{genre}の章「{title}」を{tone}500文字で執筆。"
        )
        r = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500,
            temperature=0.7,
        )
        return r.choices[0].message.content.strip()

    # ─────────────────────────
    # 簡易：本文から感情スコア推定（ダミー）
    # ─────────────────────────
    @staticmethod
    def classify_emotion(text: str) -> dict[str, float]:
        L = len(text)
        return {
            "共感": round(min(1, L / 800), 2),
            "感動": round(min(1, L / 1000), 2),
            "挑戦": round(min(1, L / 1200), 2),
        }

    # ─────────────────────────
    # 章立て自動提案メソッド（唯一版）
    # ─────────────────────────
    def propose_outline(self, genre: str, goal: str) -> list[str]:
        \"\"\"ジャンルとゴールに基づき 5 つの章タイトルを GPT で提案して返す\"\"\"
        prompt = (
            f"{genre} の読者が『{goal}』を達成するための章タイトルを "
            "5 つ、箇条書きで提案してください。"
        )
        resp = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150,
            temperature=0.5,
        )
        titles = [
            line.strip(" -\\n")
            for line in resp.choices[0].message.content.splitlines()
            if line.strip()
        ]
        return titles or ["はじめに", "第1章", "第2章", "おわりに"]
