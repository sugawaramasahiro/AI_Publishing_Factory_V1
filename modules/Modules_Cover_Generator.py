from PIL import Image, ImageDraw, ImageFont
import textwrap, os, datetime

COLOR_TABLE = {
    "共感型":  ("#FFE8E0", "#333333"),
    "感動型":  ("#FFB3AB", "#331100"),
    "論理型":  ("#E5E5E5", "#222222"),
    "挑戦型":  ("#FF4B4B", "#FFFFFF"),
    "癒し型":  ("#A4D8D8", "#003333"),
    "default": ("#FFFFFF", "#000000"),
}

def _font(sz):
    for p in (
        "C:/Windows/Fonts/arial.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ):
        if os.path.exists(p):
            return ImageFont.truetype(p, sz)
    return ImageFont.load_default()

def generate_cover(title, author, genre, emotion=None):
    bg, fg = COLOR_TABLE.get(emotion, COLOR_TABLE["default"])
    W, H = 1600, 2560
    img = Image.new("RGB", (W, H), bg)
    d   = ImageDraw.Draw(img)

    # タイトル
    t = textwrap.fill(title, 10)
    tw, th = d.multiline_textsize(t, font := _font(110), spacing=10)
    d.multiline_text(((W-tw)/2, (H-th)/2-100), t, font=font, fill=fg, spacing=10, align="center")

    # 著者
    aw, ah = d.textsize(author, font := _font(60))
    d.text(((W-aw)/2, (H-th)/2+th/2+40), author, font=font, fill=fg)

    # ジャンル
    gw, gh = d.textsize(genre, font := _font(45))
    d.text(((W-gw)/2, H-gh-120), genre, font=font, fill=fg)

    os.makedirs("output", exist_ok=True)
    fname = f"output/{''.join(c for c in title if c.isalnum() or c in ' _')}_cover_{datetime.datetime.now():%Y%m%d%H%M%S}.png"
    img.save(fname)
    return fname
