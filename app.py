from flask import Flask, Response
from vilib import Vilib
import time
import cv2

app = Flask(__name__)

def generate_frames():
    Vilib.camera_start(vflip=False, hflip=False)
    time.sleep(2)

    while True:
        frame = Vilib.img
        if frame is not None:
            ret, buffer = cv2.imencode('.jpg', frame)
            if ret:
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

@app.route('/')
def index():
    return """
    <h1>PiCar-X Camera Stream</h1>
    <img src="/video_feed" width="640">
    """

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
