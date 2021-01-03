import keyPressModule as kp
from djitellopy import tello
import numpy as np
import math
import time
import cv2

fSpeed = 117 / 10
aSpeed = 360 / 10
interval = 0.25

dInterval = fSpeed * interval
aInterval = aSpeed * interval

x, y = 500, 500
a = 0
yaw = 0
points = [(0,0), (0,0)]

kp.init()
me = tello.Tello()
me.connect()
print(me.get_battery())
global img


def getKeyboardInput():
    global x, y, a, yaw

    lr, fb, ud, yv = 0, 0, 0, 0

    # Declare the speed here
    speed = 15
    aspeed = 50
    d = 0

    # Left and right control
    if kp.getKey("LEFT"):
        lr = -speed
        d = dInterval
        a = -180

    elif kp.getKey("RIGHT"):
        lr = speed
        d = -dInterval
        a = 180

    # Forward and backward control
    if kp.getKey("UP"):
        fb = speed
        d = dInterval
        a = 270

    elif kp.getKey("DOWN"):
        fb = -speed
        d = -dInterval
        a = -90

    # Up and Down control
    if kp.getKey("w"):
        ud = speed


    elif kp.getKey("s"):
        ud = -speed

    # Left and right rotate control
    if kp.getKey("a"):
        yv = -aspeed
        yaw -= aInterval

    elif kp.getKey("d"):
        yv = aspeed
        yaw += aInterval

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

    time.sleep(0.25)
    a += yaw
    x += int(d * math.cos(math.radians(a)))
    y += int(d * math.sin(math.radians(a)))

    return [lr, fb, ud, yv, x, y]


def drawPoints(img, points):
    for point in points:
        cv2.circle(img, point, 5, (0, 0, 255), cv2.FILLED)

    cv2.circle(img, points[-1], 8, (0, 255, 0), cv2.FILLED)
    cv2.putText(img, f'({(points[-1][0] - 500) / 100}, {(points[-1][1] - 500) / 100}M',
                (points[-1][0] + 10, points[-1][1] + 30), cv2.FONT_HERSHEY_PLAIN, 1,
                (255, 0, 255), 1)


me.streamon()

while True:
    values = getKeyboardInput()
    me.send_rc_control(values[0], values[1], values[2], values[3])

    img = np.zeros((1000,1000,3), np.uint8)

    if (points[-1][0] != values[4] or points[-1][1] != values[5]):
        points.append((values[4], values[5]))

    drawPoints(img, points)
    cv2.imshow("Output", img)
    cv2.waitKey(1)
