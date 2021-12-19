import robomaster
from robomaster import robot


if __name__ == '__main__':
    tl_drone = robot.Drone()
    tl_drone.initialize()

    # 切换飞行器WiFi模式为组网模式，指定路由器SSID和密码
    tl_drone.config_sta(ssid="8675309", password="S1XTEENCANDL3$")

    tl_drone.close()
