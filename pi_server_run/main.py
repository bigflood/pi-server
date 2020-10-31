import sys
import logging
import atexit
import time
from typing import Optional, List
from flask import Flask, make_response
from pi_server.camera import Camera
import pi_server

__version__ = pi_server.__version__


class App(object):
    def __init__(self):
        self.flask_app = Flask(__name__)
        self.cam = Camera()
        self.logger = logging.getLogger()
        self.route('/', self.handle_home)
        self.route('/picam', self.handle_picam)

    def close(self):
        self.cam.close()

    def route(self, path, f):
        self.flask_app.add_url_rule(path, view_func=f)

    def run(self):
        self.flask_app.run(host='0.0.0.0')
        return 0

    def handle_home(self):
        img = self.cam.get_image()
        resp = make_response(f'''
            version={__version__}
            last_image_size={len(img.data)}
            last_image_index={img.index}
            last_image_timestamp_utc={time.asctime(time.gmtime(img.timestamp))}
            camera_clock_delay={self.cam.camera_clock_delay() / 1000000:.3f}s
            fps={self.cam.fps:.2f}
            ''')
        resp.headers['Content-Type'] = 'text/plain'
        resp.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        return resp

    def handle_picam(self):
        img = self.cam.get_image()
        resp = make_response(img.data)
        resp.headers['Content-Type'] = 'image/jpeg'
        resp.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        resp.headers['X-Image-Index'] = f'{img.index}'
        resp.headers['X-Image-Timestamp'] = f'{img.timestamp}'
        logging.getLogger().info(f'serve image: index={img.index}, {len(img.data)} bytes')
        return resp


def init_logger():
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(filename)s:%(lineno)d: %(message)s'))
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)


def main(args: Optional[List[str]] = None) -> int:
    init_logger()
    logging.getLogger().info(f'version={__version__}')

    app = App()
    atexit.register(app.close)

    return app.run()
