# simple example demonstrating how to control a Tello using your keyboard.
# For a more fully featured example see manual_control_pygame.py
#
# Use W, A, S, D for moving, E, Q for rotating and R, F for going up and down.
# When starting the script the Tello will takeoff, pressing ESC makes it land
#  and the script exit.

# 简单的演示如何用键盘控制Tello
# 欲使用全手动控制请查看 manual_control_pygame.py
#
# W, A, S, D 移动， E, Q 转向，R、F上升与下降.
# 开始运行程序时Tello会自动起飞，按ESC键降落
# 并且程序会退出
from __future__ import print_function

from djitellopy import Tello
import cv2, math, time, threading, queue

import datetime

class VideoCapture:

  def __init__(self, name):
    self.cap = cv2.VideoCapture(name)
    self.q = queue.Queue()
    t = threading.Thread(target=self._reader)
    t.daemon = True
    t.start()

  # read frames as soon as they are available, keeping only most recent one
  def _reader(self):
    while True:
      ret, frame = self.cap.read()
      if not ret:
        break
      if not self.q.empty():
        try:
          self.q.get_nowait()   # discard previous (unprocessed) frame
        except queue.Empty:
          pass
      self.q.put(frame)

  def read(self):
    return self.q.get()

# cap = VideoCapture(0)
# while True:
#   time.sleep(.5)   # simulate time between events
#   frame = cap.read()
#   cv2.imshow("frame", frame)
#   if chr(cv2.waitKey(1)&255) == 'q':
#     break

tello = Tello()
tello.connect()

tello.streamon()
frame_read = tello.get_frame_read()

tello.takeoff()

tello.enable_mission_pads()
current_pad = tello.get_mission_pad_id()

target_pad = 8

cap = VideoCapture(0)
while True and current_pad != target_pad:
    # In reality you want to display frames in a seperate thread. Otherwise
    #  they will freeze while the drone moves.
    # 在实际开发里请在另一个线程中显示摄像头画面，否则画面会在无人机移动时静止
    # img = frame_read.frame
    # cv2.imshow("drone", img)

    time.sleep(.5)  # simulate time between events
    frame = cap.read()
    cv2.imshow("frame", frame)

    key = cv2.waitKey(1) & 0xff
    if key == 27:  # ESC
        break

    elif key == ord('w'):
        tello.move_forward(30)

    elif key == ord('s'):
        tello.move_back(30)

    elif key == ord('a'):
        tello.move_left(30)

    elif key == ord('d'):
        tello.move_right(30)

    elif key == ord('l'):
        tello.rotate_clockwise(30)

    elif key == ord('j'):
        tello.rotate_counter_clockwise(30)

    elif key == ord('i'):
        tello.move_up(30)

    elif key == ord('k'):
        tello.move_down(30)

    current_pad = tello.get_mission_pad_id()

if tello.get_mission_pad_id() == target_pad:
    tello.go_xyz_speed_mid(0, 0, 20, 20, 8)

tello.land()
