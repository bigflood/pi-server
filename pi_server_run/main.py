from typing import Optional, List
from flask import Flask, send_file
from time import sleep
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
    fmt = 'jpeg'
    buf = io.BytesIO()
    with PiCamera() as camera:
        camera.rotation = 180
        camera.start_preview()
        sleep(2)
        camera.capture(buf, fmt)
        camera.stop_preview()
    buf.seek(0)
    return send_file(buf, f'image/{fmt}')


def main(args: Optional[List[str]] = None) -> int:
    logger = logging.getLogger()
    logger.info(f'version={__version__}')
    app.run(host='0.0.0.0')
    return 0
