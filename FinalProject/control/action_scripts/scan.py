from threading import Thread
from time import sleep
from twilio.rest import Client
import cv2
import imutils
import numpy as np
import time
import pytesseract
from PIL import Image
from picamera.array import PiRGBArray
from picamera import PiCamera

STATUS = "off"

class Scan():

    def __init__(self, name=""):
        self.name = name

    def scan(self, value, info):
        STATUS = "on" if value == "start" else "off"
        if STATUS == "on" and value == "start":
            thread = Thread(target = threadFunction, args=(info))
            thread.start()
        result = f"{self.name} scanning turned {STATUS} "
        return result

def threadFunction(type, color, license):
    while(STATUS == "on"):
        lookingFor = license

        camera = PiCamera()
        camera.resolution = (640, 480)
        rawCapture = PiRGBArray(camera, size=(640, 480))
        for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
            image = frame.array
            time.sleep(1)
            key = cv2.waitKey(1) & 0xFF
            rawCapture.truncate(0)
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # convert to grey scale
            gray = cv2.bilateralFilter(gray, 11, 17, 17)  # Blur to reduce noise
            edged = cv2.Canny(gray, 30, 200)  # Perform Edge detection
            cnts = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            cnts = imutils.grab_contours(cnts)
            cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:10]
            screenCnt = None
            for c in cnts:
                peri = cv2.arcLength(c, True)
                approx = cv2.approxPolyDP(c, 0.018 * peri, True)
                if len(approx) == 4:
                    screenCnt = approx
                    break
            if screenCnt is None:
                detected = 0
                continue
            else:
                detected = 1
            if detected == 1:
                cv2.drawContours(image, [screenCnt], -1, (0, 255, 0), 3)
            mask = np.zeros(gray.shape, np.uint8)
            new_image = cv2.drawContours(
                mask,
                [screenCnt],
                0,
                255,
                -1,
            )
            new_image = cv2.bitwise_and(image, image, mask=mask)
            (x, y) = np.where(mask == 255)
            (topx, topy) = (np.min(x), np.min(y))
            (bottomx, bottomy) = (np.max(x), np.max(y))
            Cropped = gray[topx : bottomx + 1, topy : bottomy + 1]
            text = pytesseract.image_to_string(Cropped, config="--psm 11")
            if(lookingFor in text):
                STATUS = "off"
                break
        cv2.destroyAllWindows()
    #sleep(10)
    #STATUS = "off"
    # after finish
    # Set environment variables for your credentials (am lazy c:)
    # Read more at http://twil.io/secure
    account_sid = "ACee2fd0f1586d4ca13f67e265e50a58a5"
    auth_token = "f3603044422224d92baa45f4bfc4887a"
    client = Client(account_sid, auth_token)
    message = client.messages.create(
    body="We found a {} {} vehicle with license plate {} at: {}"
        .format(color, type, license, "CWRU"),# location will be taken from GPS 
    from_="+18775255017",
    to="+14404977348")# this will be a designated authority number
