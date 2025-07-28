import subprocess
import threading
import webbrowser
import time
import requests
import sys



LMSTUDIO_URL = "http://localhost:1234/v1/models"
FLASK_URL = "http://localhost:5000"

def is_lmstudio_running():
    try:
        response = requests.get(LMSTUDIO_URL, timeout=2)
        return response.status_code == 200
    except requests.RequestException:
        return False

def start_lmstudio():
    if not is_lmstudio_running():
        print("Starting LM Studio server...")
        subprocess.Popen(["lms", "server", "start"], shell=True)
        for _ in range(10):
            if is_lmstudio_running():
                print("LM Studio is now running.")
                return
            time.sleep(1)
        print("Warning: LM Studio did not start within expected time.")
    else:
        print("LM Studio is already running.")

def wait_for_flask():
    print("Waiting for Flask app to start...")
    for _ in range(30):
        try:
            response = requests.get(FLASK_URL, timeout=2)
            if response.status_code == 200:
                print("Flask app is running.")
                return True
        except requests.RequestException:
            pass
        time.sleep(1)
    print("Error: Flask app did not start.")
    return False

def open_browser():
    if wait_for_flask():
        webbrowser.open(FLASK_URL)

def run_flask_app():
    try:
        subprocess.run([sys.executable, "app.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Flask app exited with error: {e}")

if __name__ == "__main__":
    threading.Thread(target=start_lmstudio).start()
    threading.Thread(target=open_browser).start()
    run_flask_app()
