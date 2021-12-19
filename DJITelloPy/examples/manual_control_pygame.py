from djitellopy import Tello
import cv2
import pygame
import numpy as np
import time
from robomaster import robot
from tkinter import *
from tkinter import messagebox

# Speed of the drone
# 无人机的速度
S = 60
# Frames per second of the pygame window display
# A low number also results in input lag, as input information is processed once per frame.
# pygame窗口显示的帧数
# 较低的帧数会导致输入延迟，因为一帧只会处理一次输入信息
FPS = 120


class FrontEnd(object):
    """ Maintains the Tello display and moves it through the keyboard keys.
        Press escape key to quit.
        The controls are:
            - T: Takeoff
            - L: Land
            - Arrow keys: Forward, backward, left and right.
            - A and D: Counter clockwise and clockwise rotations (yaw)
            - W and S: Up and down.
            - M+L Locate MissionPad and Lgand

        保持Tello画面显示并用键盘移动它
        按下ESC键退出
        操作说明：
            T：起飞
            L：降落
            方向键：前后左右
            A和D：逆时针与顺时针转向
            W和S：上升与下降

    """

    def __init__(self):
        # Init pygame
        # 初始化pygame
        pygame.init()

        # Creat pygame window
        # 创建pygame窗口
        pygame.display.set_caption("Tello video stream")
        self.screen = pygame.display.set_mode([960, 720])

        # Init Tello object that interacts with the Tello drone
        # 初始化与Tello交互的Tello对象
        self.tello = Tello()

        # Drone velocities between -100~100
        # 无人机各方向速度在-100~100之间
        self.for_back_velocity = 0
        self.left_right_velocity = 0
        self.up_down_velocity = 0
        self.yaw_velocity = 0
        self.speed = 10

        # Drone navigation recording

        self.nav_record = []

        self.send_rc_control = False

        # create update timer
        # 创建上传定时器
        pygame.time.set_timer(pygame.USEREVENT + 1, 1000 // FPS)

    # target_pad = 8

    def get_tof_distance(self, tl_drone):
        # returns distance in mm 8192 default if out of range
        # for i in range(0, 10):
        tof_info = tl_drone.sensor.get_ext_tof()

        # print("ext tof: {0}".format(tof_info))
        return tof_info

    def object_detected_distance(self, tl_drone, distance_tolerance=609):
        tof_distance = self.get_tof_distance(tl_drone)
        # time.sleep(0.5)
        if tof_distance < distance_tolerance:
            return True
        return False

    def land_on_mission_pad(self):
        # self.tello.enable_mission_pads()
        # self.tello.set_mission_pad_detection_direction(1)
        count = 0
        while count < 5:
            # self.tello.rotate_counter_clockwise(90)
            try:
                current_pad = self.tello.get_mission_pad_id()
            except EXCEPTION as ex:
                current_pad = -1
                print(ex)
            # messagebox.OK()
            # Go to any pad
            if current_pad != -1:
                # messagebox.showinfo("LANDING on MissionPad: " + str(current_pad))
                pygame.display.set_caption("LANDING on MissionPad: " + str(current_pad))
                # self.tello.rotate_clockwise(90)
                try:
                    self.tello.rotate_clockwise(90)
                    self.tello.go_xyz_speed_mid(0, 0, 40, 25, current_pad)
                    self.tello.land()
                    # self.tello.disable_mission_pads()
                    self.send_rc_control = False
                    break
                except:
                    continue
                # break
            count += 1
        # messagebox.OK()
        # self.tello.disable_mission_pads()
        # self.tello.streamon()

    def run(self):

        # tl_drone = robot.Drone()
        # tl_drone.initialize()
        self.tello.connect()

        # self.tello.turn_motor_on()
        self.tello.set_speed(self.speed)

        # self.tello.set_video_bitrate(Tello.BITRATE_AUTO)
        # self.tello.set_video_resolution(Tello.RESOLUTION_480P)
        # In case streaming is on. This happens when we quit this program without the escape key.
        # 防止视频流已开启。这会在不使用ESC键退出的情况下发生。
        self.tello.streamoff()
        self.tello.streamon()
        # self.tello.enable_mission_pads()

        frame_read = self.tello.get_frame_read()
        should_stop = False
        # distance_tolerance = 609 #mm

        while not should_stop:
            for event in pygame.event.get():
                if event.type == pygame.USEREVENT + 1:
                    self.update()
                elif event.type == pygame.QUIT:
                    should_stop = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        should_stop = True
                    else:
                        self.keydown(event.key)
                elif event.type == pygame.KEYUP:
                    self.keyup(event.key)

            if frame_read.stopped:
                break

            self.screen.fill([0, 0, 0])

            frame = frame_read.frame
            # battery n. 电池
            text = "Battery: {}%".format(self.tello.get_battery())
            cv2.putText(frame, text, (5, 720 - 5),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = np.rot90(frame)
            frame = np.flipud(frame)

            frame = pygame.surfarray.make_surface(frame)
            self.screen.blit(frame, (0, 0))
            pygame.display.update()

            time.sleep(1 / FPS)

        # Call it always before finishing. To deallocate resources.
        # 通常在结束前调用它以释放资源
        # self.tello.turn_motor_off()
        self.tello.end()

    def keydown(self, key):
        """ Update velocities based on key pressed
        Arguments:
            key: pygame key

        基于键的按下上传各个方向的速度
        参数：
            key：pygame事件循环中的键事件
        """
        if key == pygame.K_UP:  # set forward velocity
            self.for_back_velocity = S
        elif key == pygame.K_DOWN:  # set backward velocity
            self.for_back_velocity = -S
        elif key == pygame.K_LEFT:  # set left velocity
            self.left_right_velocity = -S
        elif key == pygame.K_RIGHT:  # set right velocity
            self.left_right_velocity = S
        elif key == pygame.K_w:  # set up velocity
            self.up_down_velocity = S
        elif key == pygame.K_s:  # set down velocity
            self.up_down_velocity = -S
        elif key == pygame.K_a:  # set yaw counter clockwise velocity
            self.yaw_velocity = -S
        elif key == pygame.K_d:  # set yaw clockwise velocity
            self.yaw_velocity = S
        elif key == pygame.K_f:
            self.tello.flip_back()
        elif key == pygame.K_m:  # enable mission pad detection and landing feature
            # self.tello.streamoff()
            self.tello.enable_mission_pads()
            self.land_on_mission_pad()
            self.tello.disable_mission_pads()

    def keyup(self, key):
        """ Update velocities based on key released
        Arguments:
            key: pygame key

        基于键的松开上传各个方向的速度
        参数：
            key：pygame事件循环中的键事件
        """
        if key == pygame.K_UP or key == pygame.K_DOWN:  # set zero forward/backward velocity
            self.for_back_velocity = 0
        elif key == pygame.K_LEFT or key == pygame.K_RIGHT:  # set zero left/right velocity
            self.left_right_velocity = 0
        elif key == pygame.K_w or key == pygame.K_s:  # set zero up/down velocity
            self.up_down_velocity = 0
        elif key == pygame.K_a or key == pygame.K_d:  # set zero yaw velocity
            self.yaw_velocity = 0
        elif key == pygame.K_t:  # takeoff
            self.tello.takeoff()
            self.send_rc_control = True
        elif key == pygame.K_l:  # land
            self.tello.land()
            self.send_rc_control = False

    def update(self):
        """ Update routine. Send velocities to Tello.

            向Tello发送各方向速度信息
        """
        if self.send_rc_control:
            self.tello.send_rc_control(self.left_right_velocity, self.for_back_velocity,
                                       self.up_down_velocity, self.yaw_velocity)

            self.nav_record.append()


def main():
    frontend = FrontEnd()

    # run frontend

    frontend.run()


if __name__ == '__main__':
    main()
