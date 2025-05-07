from flask import Flask
from threading import Thread
import time
from monitor import check_stock_button

app = Flask(__name__)


# Background job function
def run_checker():
    while True:
        print("🔄 Running periodic check...")
        check_stock_button()
        time.sleep(60)  # Every 60 seconds


# Start the background thread right away
Thread(target=run_checker, daemon=True).start()


@app.route("/")
def index():
    return "✅ Monitor is running."


@app.route("/check")
def manual_check():
    check_stock_button()
    return "✅ Manual check complete."


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
