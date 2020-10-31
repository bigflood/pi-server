import io
import time
import logging
from threading import Thread, Event
from picamera import PiCamera


class Camera(object):
    def __init__(self):
        self.logger = logging.getLogger()
        # https://picamera.readthedocs.io/en/release-1.10/api_camera.html
        self.camera = PiCamera(
            framerate_range=(0.16666, 10),
            resolution=(1640, 1232),
            clock_mode='raw',
        )
        self.camera.rotation = 180
        # self.logger.info(f'camera: framerate={self.camera.framerate} framerate_delta={self.camera.framerate_delta} framerate_range={self.camera.framerate_range}')
        self.last_image = None
        self.fps = 0.0
        self.image_count = 0
        self.last_request_time = time.time()

        self.cur_image_buf = io.BytesIO()
        self.image_timestamps = []

        self.ready_event = Event()
        self.stop_event = Event()
        self.stop_flag = False
        self.thread = Thread(target=self.run_loop)
        self.thread.start()

    def close(self):
        self.logger.info('close..')
        self.stop_flag = True
        self.stop_event.set()
        self.thread.join()
        self.camera.close()

    def run_loop(self):
        self.camera.start_preview()
        time.sleep(2)
        # https://picamera.readthedocs.io/en/release-1.10/api_camera.html#picamera.camera.PiCamera.capture
        # https://picamera.readthedocs.io/en/release-1.13/recipes2.html#rapid-capture-and-processing
        self.logger.info('start recording..')
        self.camera.start_recording(self, format='mjpeg')
        self.stop_event.wait()
        self.logger.info('stop recording..')
        self.camera.stop_recording()
        self.camera.stop_preview()
        self.logger.info('end run_loop')

    def write(self, buf):
        if buf.startswith(b'\xff\xd8'):
            ts = time.time()
            self.last_image = Image(self.cur_image_buf.getvalue(), self.image_count, ts)
            self.update_fps(ts)
            self.image_count += 1
            self.cur_image_buf = io.BytesIO()
            self.ready_event.set()
            self.sleep_frame()
        self.cur_image_buf.write(buf)

    def sleep_frame(self):
        end_ts = time.time() + 60
        step = 0.1
        while not self.need_next_image() and time.time() < end_ts and not self.stop_flag:
            time.sleep(step)

    def need_next_image(self):
        return time.time() - self.last_request_time < 5 * 60

    def update_fps(self, ts):
        self.image_timestamps.append(ts)
        self.image_timestamps = self.image_timestamps[-100:]
        if len(self.image_timestamps) >= 2:
            d = self.image_timestamps[-1] - self.image_timestamps[0]
            if d > 0.0001:
                self.fps = (len(self.image_timestamps) - 1) / d

    def get_image(self):
        self.last_request_time = time.time()
        self.ready_event.wait()
        return self.last_image

    def camera_clock_delay(self):
        t1 = self.camera.timestamp
        f = self.camera.frame
        if not f:
            return 0
        t2 = f.timestamp
        if not t2:
            return 0
        return t1 - t2


class Image(object):
    def __init__(self, data, index, timestamp):
        self.data = data
        self.index = index
        self.timestamp = timestamp
