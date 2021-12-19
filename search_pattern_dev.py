# -*-coding:utf-8-*-
# Copyright (c) 2020 DJI.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License in the file LICENSE.txt or at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


# from robomaster import *
from djitellopy.tello import *
from robomaster import robot

# def get_mission_pad_id(self):
#
#
#
#     mission_pad_id = robot.TelloStatusSubject.get_status(self, self._dds_proto.DDS_PAD_MID_FLAG)
#
#     return mission_pad_id
#


if __name__ == '__main__':

    status_subject = robot.TelloStatusSubject()

    # tl_drone = robot.Drone()
    # tl_drone.initialize()

    tello = Tello()
    tello.connect()

    tello.enable_mission_pads()

    # tl_flight = tl_drone.flight

    # tl_flight.mission_pad_on()


    # create and connect
    # 创建Tello对象并连接

    # configure drone
    # 设置无人机
    # tello.enable_mission_pads()
    tello.set_mission_pad_detection_direction(1)  # forward detection only  只识别前方

    # 起飞
    # tello.takeoff()

    # tl_flight.takeoff().wait_for_completed()
    tello.takeoff()
    # tello.go_xyz_speed_mid(x=0, y=0, z=50, speed=20, mid=1)

    pad = tello.get_mission_pad_id()

    # detect and react to pads until we see pad #1
    # 发现并识别挑战卡直到看见1号挑战卡

    distance_ft = 1
    distance_cm = distance_ft * 30.48

    distance_multiplier = 1

    count = 0

    current_distance_multiplier = 1
    # 1 ft =  30.48 cm

    while pad != 8:

        if count == 2:
            distance_multiplier += 1
            count = 0
            tello.rotate_clockwise(90)
        else:
            count += 1

            tello.move_forward(int(distance_cm * distance_multiplier))


        # tl_flight.forward(distance= 10)
        # if pad == 3:
        #     tello.move_forward(50)
        #     tello.rotate_clockwise(90)
        #
        # if pad == 4:
        #     tello.move_up(30)
        #     tello.flip_forward()

        pad = tello.get_mission_pad_id()

    # tl_flight.go(x=0, y=0, z=22, speed=22, mid="m8").wait_for_completed()
    tello.go_xyz_speed_mid(x=0, y=0, z=22, speed=22, mid=8)

    # graceful termination
    # 安全结束程序

    # while get_mission_pad_id(tl_drone) != 8:
    #     tl_flight.forward(speed=30)
    # tl_flight.go(x=50, y=0, z=100, speed=30, mid="m1").wait_for_completed()
    # tl_flight.go(x=0, y=0, z=22, speed=22, mid="m8").wait_for_completed()
    # tl_flight.go(x=-50, y=0, z=100, speed=30, mid="m8").wait_for_completed()
    # tl_flight.go(x=-50, y=0, z=30, speed=30, mid="m8").wait_for_completed()
    # tl_flight.go(x=0, y=0, z=120, speed=30, mid="m1").wait_for_completed()
    # tl_flight.go(x=30, y=0, z=100, speed=30, mid="m1").wait_for_completed()

    # tl_flight.flip_backward().wait_for_completed()
    # tl_flight.flip_forwards().wait_for_completed()

    # tl_flight.go(x=0, y=0, z=50, speed=30, mid="m1").wait_for_completed()


    # tl_flight.go(x=30, y=0, z=30, speed=40, mid="m1").wait_for_completed()

    # tl_flight.go(x=0, y=0, z=25, speed=20, mid="m1").wait_for_completed()

    # tl_flight.go(x=0, y=0, z=25, speed=10, mid="m1").wait_for_completed()



    # tl_flight.go(x=0, y=0, z=22, speed=30, mid="m1").wait_for_completed()

    # tl_flight.forward(distance=150).wait_for_completed()
    # tl_flight.backward(distance=145).wait_for_completed()
    #
    # # 曲线飞行
    # tl_flight.curve(x1=60, y1=60, z1=0, x2=120, y2=0, z2=30, speed=30).wait_for_completed()
    # tl_flight.flip_forward().wait_for_completed()
    # tl_flight.flip_backward().wait_for_completed()
    # tl_flight.flip_left().wait_for_completed()
    # tl_flight.flip_left().wait_for_completed()
    # tl_flight.flip_right().wait_for_completed()
    # tl_flight.flip_right().wait_for_completed()
    # tl_flight.curve(x1=-60, y1=60, z1=0, x2=-120, y2=0, z2=-30, speed=30).wait_for_completed()



    # 降落
    # tl_flight.land().wait_for_completed()
    #
    # tl_flight.mission_pad_off()

    tello.land()

    tello.disable_mission_pads()

    tl_drone.close()
