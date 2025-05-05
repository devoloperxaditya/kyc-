# app.py
from flask import Flask, request, send_file
from flask_cors import CORS
from PIL import Image
import cv2
import numpy as np
import os

app = Flask(__name__)
CORS(app)  # allow frontend access

@app.route('/')
def home():
    return open("index.html").read()

@app.route('/blink', methods=['POST'])
def blink():
    img_file = request.files['image']
    img = Image.open(img_file).convert('RGB')
    img = np.array(img)

    # Simulate eye blink by darkening eye area
    h, w, _ = img.shape
    blink_frames = []
    for i in range(5):
        frame = img.copy()
        cv2.rectangle(frame, (w//3, h//3), (2*w//3, h//2), (0,0,0), -1)
        blink_frames.append(frame)
        blink_frames.append(img)  # back to original

    # Save to video
    out_path = "static/output.mp4"
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(out_path, fourcc, 2, (w, h))
    for f in blink_frames:
        out.write(f)
    out.release()

    return send_file(out_path, mimetype='video/mp4')

if __name__ == '__main__':
    os.makedirs("static", exist_ok=True)
    app.run(debug=True)

