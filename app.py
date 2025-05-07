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
        time.sleep(60)  # Run every 1 minute

print("App is:", type(app))  # Should show <class 'flask.app.Flask'>

@app.before_first_request
def start_background_thread():
    thread = Thread(target=run_checker, daemon=True)
    thread.start()
    print("🚀 Background thread started.")

@app.route("/")
def index():
    return "✅ Monitor is running in the background."

@app.route("/check")
def check_now():
    check_stock_button()
    return "✅ Manual check done."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
