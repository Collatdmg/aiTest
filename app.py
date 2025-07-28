import os
import re
import requests
import markdown
from flask import Flask, request, render_template, jsonify
from PIL import Image
from uuid import uuid4
import pytesseract

pytesseract.pytesseract.tesseract_cmd = #pathtotesseract if tesseract is not in the system PATH

app = Flask(__name__)
app.secret_key = os.urandom(24)

def query_lm_studio(prompt):
    url = "http://localhost:1234/v1/chat/completions"
    headers = {"Content-Type": "application/json"}
    payload = {
        "model": "llama-3.1-8b",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    }
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except requests.exceptions.RequestException as e:
        return f"Error communicating with LM Studio: {e}"

def sanitize_input(user_input):
    forbidden_phrases = ["forget", "ignore", "override", "bypass", "reset"]
    for phrase in forbidden_phrases:
        user_input = re.sub(rf"\b{phrase}\b", "[filtered]", user_input, flags=re.IGNORECASE)
    return user_input

def extract_text_from_image(image_path):
    image = Image.open(image_path)
    return pytesseract.image_to_string(image)

@app.route("/")
def index():
    return render_template("chat.html")

@app.route("/async-message", methods=["POST"])
def async_message():
    user_input = request.form.get("message", "")
    user_input = sanitize_input(user_input)

    if "file" in request.files:
        uploaded_file = request.files["file"]
        if uploaded_file and uploaded_file.filename:
            filename = uploaded_file.filename
            ext = os.path.splitext(filename)[1].lower()

            if ext in [".png", ".jpg", ".jpeg"]:
                image_path = "temp_image.png"
                uploaded_file.save(image_path)
                file_text = extract_text_from_image(image_path)
                os.remove(image_path)
                user_input += f"\n[Image Text]: {file_text}"

            elif ext in [".txt", ".py", ".js", ".html", ".css", ".json", ".csv"]:
                file_content = uploaded_file.read().decode("utf-8", errors="ignore")
                user_input += f"\n[File Content from {filename}]:\n{file_content}"

    prompt = f"User: {user_input}\nAssistant:"
    raw_response = query_lm_studio(prompt)
    bot_response = markdown.markdown(raw_response)

    return jsonify({"bot": bot_response})

if __name__ == "__main__":
    app.run(debug=True)
