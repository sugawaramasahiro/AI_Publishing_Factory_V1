import openai
from typing import List

SYSTEM_PROMPT = \"\"\"\
あなたはベストセラー編集者です。与えられた書籍タイトルをもとに、
読者が抱えるであろう「悩み」と、それを解決したときに得られる
「理想の未来」をそれぞれ30個ずつ、シンプルな日本語の箇条書きで出力してください。
\"\"\"

def _call_openai(messages: list[dict]) -> str:
    resp = openai.ChatCompletion.create(
        model=\"gpt-4o-mini\",
        temperature=0.8,
        messages=messages,
    )
    return resp.choices[0].message.content.strip()

def _split(text: str) -> list[str]:
    return [l.lstrip(\"・-–—* \").strip() for l in text.splitlines() if l.strip()]

def generate_pain_and_gain(title: str) -> tuple[list[str], list[str]]:
    user_prompt = f\"タイトル: {title}\"
    content = _call_openai(
        [
            {\"role\": \"system\", \"content\": SYSTEM_PROMPT},
            {\"role\": \"user\",   \"content\": user_prompt},
        ]
    )
    pains, gains = content.split(\"\\n\\n\")[:2]
    return _split(pains), _split(gains)
