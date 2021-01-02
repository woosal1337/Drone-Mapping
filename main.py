import keyPressModule as kp
from djitellopy import tello
import time
import cv2

kp.init()
me = tello.Tello()
me.connect()
print(me.get_battery())
global img

def getKeyboardInput():
    lr, fb, ud, yv = 0, 0, 0, 0

    # Declare the speed here
    speed = 75

    # Left and right control
    if kp.getKey("LEFT"):
        lr = -speed
    elif kp.getKey("RIGHT"):
        lr = speed

    # Forward and backward control
    if kp.getKey("UP"):
        fb = speed
    elif kp.getKey("DOWN"):
        fb = -speed

    # Up and Down control
    if kp.getKey("w"):
        ud = speed
    elif kp.getKey("s"):
        ud = -speed

    # Left and right rotate control
    if kp.getKey("a"):
        yv = -speed
    elif kp.getKey("d"):
        yv = speed

    # Taking off
    if kp.getKey("t"):
        me.takeoff()
        print('TAKING OFF')

    # Landing
    if kp.getKey("q"):
        me.land()
        print("LANDING")

    # Save the captured images
    if kp.getKey("z"):
        cv2.imwrite(f"Media/{time.time()}.jpg", img)
        time.sleep(0.35)

    return [lr, fb, ud, yv]


me.streamon()

while True:
    values = getKeyboardInput()
    me.send_rc_control(values[0], values[1], values[2], values[3])

    img = me.get_frame_read().frame
    img = cv2.resize(img, (360,240))
    cv2.imshow("Image", img)
    cv2.waitKey(1)
