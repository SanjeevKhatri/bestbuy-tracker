import time
from playwright.sync_api import sync_playwright
import smtplib
from email.mime.text import MIMEText
import os

# --- Config from environment variables ---
URL = "https://www.bestbuy.com/site/nintendo-switch-2-mario-kart-world-bundle-multi/6614325.p?skuId=6614325"
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
TO_EMAIL = os.getenv("TO_EMAIL")

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
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Set user-agent to avoid bot blocking
        page.set_extra_http_headers({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        })
        print("🔄 Checking Best Buy...")
        try:
        page.goto(URL, timeout=120000, wait_until="domcontentloaded")
            button = page.locator("button.add-to-cart-button").first
            text = button.text_content().strip().lower()
            print(f"🟡 Button Text: '{text}'")

            if text.lower() in ["add to cart", "pre-order"]:
                print("✅ Product might be available!")
                send_email_alert()
            else:
                print("❌ Still unavailable (Button shows '{}').".format(text))

        except Exception as e:
            print("⚠️ Could not read button text:", e)

        browser.close()

# 🔁 Loop forever, every 60 seconds
while True:
check_stock_button()
    time.sleep(60)
