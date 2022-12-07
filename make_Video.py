import os
import time
from PIL import ImageGrab

from cv2 import VideoWriter_fourcc, VideoWriter, cvtColor, COLOR_RGB2BGR, CAP_PROP_FPS, \
    CAP_PROP_FRAME_COUNT
import numpy as np
from pynput import keyboard
from pynput.keyboard import Controller, Key
import threading


class MakeVideo(object):
    def __init__(self, name, dir: str):
        # self.make_dir()
        self.name = name
        self.width, self.height = ImageGrab.grab().size
        self.fourcc = VideoWriter_fourcc('m', 'p', '4', 'v')
        self.video = VideoWriter(f'{dir}/{self.name}.mp4', self.fourcc, 5, ImageGrab.grab().size)

        self.fps = self.video.get(CAP_PROP_FPS)
        self.frames = self.video.get(CAP_PROP_FRAME_COUNT)
        self.flag = False

    @classmethod
    def make_dir(cls):
        video_dir = f"video"
        if not os.path.exists(video_dir):
            os.makedirs(video_dir)

    def write_video(self):
        while True:
            if self.flag:
                self.video.release()
                break
            img = ImageGrab.grab()
            imm = cvtColor(np.array(img), COLOR_RGB2BGR)  # 转为opencv的BGR模式
            # 开始录屏
            self.video.write(imm)

    def close(self, key):
        if key == keyboard.Key.home:
            self.flag = True
            return False  # 返回False，键盘监听结束


def start(name="", dir=""):
    if name == "":
        name = time.time()
    make_video = MakeVideo(name, dir)
    th = threading.Thread(target=make_video.write_video)
    th.start()
    with keyboard.Listener(on_press=make_video.close) as listener:
        listener.join()


def close():
    contr = Controller()
    contr.press(Key.home)

    # if __name__ == '__main__':
    #     start = threading.Thread(target=start, args=(1111,))
    #     start.start()
    # time.sleep(3)
    # close = threading.Thread(target=close)
    # close.start()
