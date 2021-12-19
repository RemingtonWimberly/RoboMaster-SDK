
import DJITelloPy.examples.manual_control_pygame as manual_control
from djitellopy.tello import *


def main():
    control = manual_control.FrontEnd()
    control.run()

if __name__ == '__main__':
    main()
