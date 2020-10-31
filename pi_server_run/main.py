from typing import Optional, List
from flask import Flask, send_file, request
from time import sleep, time
import io
import logging
from picamera import PiCamera
import pi_server

__version__ = pi_server.__version__

app = Flask(__name__)


@app.route('/')
def hello_world():
    return f'Hello World! {__version__}'


@app.route('/picam')
def serve_picamera_image():
    jpeg_quality = int(request.args.get('q') or 50)
    fmt = 'jpeg'
    buf = io.BytesIO()
    # https://picamera.readthedocs.io/en/release-1.10/api_camera.html
    with PiCamera() as camera:
        camera.resolution = (2592, 1944)
        camera.rotation = 180
        camera.start_preview()
        sleep(2)
        # https://picamera.readthedocs.io/en/release-1.10/api_camera.html#picamera.camera.PiCamera.capture
        start_time = time()
        camera.capture(buf, fmt, quality=jpeg_quality)
        camera.stop_preview()
    app.logger.info(f'capture: time={time()-start_time}, size={buf.tell()}, jpeg_quality={jpeg_quality}')
    buf.seek(0)
    return send_file(buf, f'image/{fmt}')


def main(args: Optional[List[str]] = None) -> int:
    app.logger.setLevel(logging.INFO)
    app.logger.info(f'version={__version__}')
    app.run(host='0.0.0.0')
    return 0
