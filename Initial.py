import robomaster.config

from robomaster import robot

# robomaster.config.LOCAL_IP_STR = "192.168.0.168"

tl_drone = robot.Drone()


tl_drone.initialize()

# tl_flight = tl_drone.flight

drone_version = tl_drone.get_sdk_version()

print("Drone sdk version: {0}".format(drone_version))

SN = tl_drone.get_sn()
print(SN)


tl_drone.close()


