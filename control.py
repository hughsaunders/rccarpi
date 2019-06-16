#import evdev
import time
from evdev import InputDevice, categorize, ecodes

from gpiozero import LED, DigitalOutputDevice

class Motor():
    def __init__(this, pin1, pin2):
       this.pin1 = DigitalOutputDevice(pin1)
       this.pin2 = DigitalOutputDevice(pin2)

    def forward(this):
        this.pin1.on()
        this.pin2.off()

    def reverse(this):
        this.pin1.off()
        this.pin2.on()

    def stop(this):
        this.pin1.off()
        this.pin2.off()


# Gamepad Event Constants
EVT_TYPE_BUTTON = 1
EVT_TYPE_AXIS = 3
EVT_BTN_PRESS = 1
EVT_BTN_RELEASE = 0
EVT_BTN_X = 307 # Left
EVT_BTN_Y = 308 # Test LED 2
EVT_BTN_B = 305 # Right
EVT_BTN_A = 304 # Test LED ON/OFF
EVT_AXIS_Y = 1 # forweard/reverse axis
EVT_Y_FWD = 0
EVT_Y_STOP = 127
EVT_Y_REV = 255
    
#creates object 'gamepad' to store the data
#you can call it whatever you like
gamepad = InputDevice('/dev/input/event0')


# Pi Pinout
#   3V3  (1) (2)  5V
# GPIO2  (3) (4)  5V
# GPIO3  (5) (6)  GND
# GPIO4  (7) (8)  GPIO14
#   GND  (9) (10) GPIO15
#GPIO17 (11) (12) GPIO18
#GPIO27 (13) (14) GND
#GPIO22 (15) (16) GPIO23
#   3V3 (17) (18) GPIO24
#GPIO10 (19) (20) GND
# GPIO9 (21) (22) GPIO25
#GPIO11 (23) (24) GPIO8
#   GND (25) (26) GPIO7
# GPIO0 (27) (28) GPIO1
# GPIO5 (29) (30) GND
# GPIO6 (31) (32) GPIO12
#GPIO13 (33) (34) GND
#GPIO19 (35) (36) GPIO16
#GPIO26 (37) (38) GPIO20
#   GND (39) (40) GPIO21

# Create Motor Object
drive = Motor(26,20)
steer = Motor(19,16)

test_led = LED(2)
test_led_2 = LED(15)

#prints out device info at start
print(gamepad)

def reset():
    print("Resetting GPIO pins")
    test_led.off();
    test_led_2.off();
    drive.stop()
    steer.stop()


#evdev takes care of polling the controller in a loop
def control_loop():
    for event in gamepad.read_loop():
        if event.type == EVT_TYPE_AXIS and event.code == EVT_AXIS_Y:
            if event.value == EVT_Y_FWD:
                print("Drive Forwards")
                drive.forward()
            elif event.value == EVT_Y_STOP:
                print("Drive Stop")
                drive.stop()
            elif event.value == EVT_Y_REV:
                print("Drive Backwards")
                drive.reverse()
        elif event.type == EVT_TYPE_BUTTON:
            if event.code == EVT_BTN_X:
                if event.value == EVT_BTN_PRESS:
                    print("Steer Left")
                    steer.forward();
                else:
                    print("Steer Straight")
                    steer.stop()
            elif event.code == EVT_BTN_B:
                if event.value == EVT_BTN_PRESS:
                    print("Steer Right")
                    steer.reverse();
                else:
                    print("Steer Straight")
                    steer.stop()
            elif event.code == EVT_BTN_A:
                if event.value == EVT_BTN_PRESS:
                    print("test LED on")
                    test_led.on();
                else:
                    print("test LED off")
                    test_led.off();
            elif event.code == EVT_BTN_Y:
                if event.value == EVT_BTN_PRESS:
                    print("test LED 2on")
                    test_led_2.on();
                else:
                    print("test LED 2 off")
                    test_led_2.off();

            else:
                if event.value == EVT_BTN_PRESS:
                    print("Unknown Button Press "+str(event.code))
                else:
                    print("Unknown Button Release "+str(event.code))

def main():
    reset()
    try:
        control_loop()
    finally:
        reset()

main()
