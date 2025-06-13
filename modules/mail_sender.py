import smtplib
from email.mime.text import MIMEText

def send_mail(email, title):
    sender = "tan5mpt@gmail.com"
    password = "mgiapdmpnugqnyqz"

    subject = f"📘『{title}』が完成しました！"
    body = f"こんにちは！\n電子書籍『{title}』の生成が完了しました。\nおめでとうございます📘✨"

    msg = MIMEText(body, "plain", "utf-8")
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = email

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender, password)
            server.send_message(msg)
            print("✉️ メール送信成功！")
    except Exception as e:
        print(f"⚠️ メール送信失敗: {e}")
