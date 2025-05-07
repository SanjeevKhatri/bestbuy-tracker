import time
from playwright.sync_api import sync_playwright
import smtplib
from email.mime.text import MIMEText
import os
import sys

# --- Config from environment variables or hardcoded fallback (for local dev) ---
URL = os.getenv("SWITCH_URL",
                "https://www.bestbuy.com/site/nintendo-switch-2-mario-kart-world-bundle-multi/6614325.p?skuId=6614325")
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS", "your_email@gmail.com")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", "your_app_password")
TO_EMAIL = os.getenv("TO_EMAIL", "recipient_email@gmail.com")


def send_email_alert():
    msg = MIMEText(f"The Nintendo Switch might be available!\n\nCheck here: {URL}")
    msg["Subject"] = "🎮 Best Buy Alert: Switch In Stock!"
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = TO_EMAIL

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)
            print("📬 Email sent!")
    except Exception as e:
        print("❌ Failed to send email:", e)


def check_stock_button():
    with sync_playwright() as p:
        try:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            page.set_extra_http_headers({
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
            })

            print("🔄 Checking Best Buy...")
            page.goto(URL, timeout=120000, wait_until="domcontentloaded")

            button = page.locator("button.add-to-cart-button").first
            text = button.text_content().strip().lower() if button else ""

            print(f"🟡 Button Text: '{text}'")

            if text in ["add to cart", "pre-order"]:
                print("✅ Product might be available!")
                send_email_alert()
            else:
                print(f"❌ Still unavailable (Button shows '{text}').")

        except Exception as e:
            print("⚠️ Could not complete check:", e)

        finally:
            browser.close()


if __name__ == "__main__":
    while True:
        check_stock_button()
        time.sleep(60)
