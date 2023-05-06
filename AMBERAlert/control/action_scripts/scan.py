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
import gps
from geopy.geocoders import Nominatim

STATUS = "off"

class Scan():

    def __init__(self, name=""):
        self.name = name

    def scan(self, value, info):
        global STATUS
        STATUS = "on" if value == "start" else "off"
        if STATUS == "on" and value == "start":
            thread = Thread(target = threadFunction, args=(info))
            thread.start()
        result = f"{self.name} scanning turned {STATUS} "
        return result

def threadFunction(type, color, license):
    global STATUS
    GPS = gps.gps(mode=gps.WATCH_ENABLE)

    # Scan for license plate
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
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            gray = cv2.bilateralFilter(gray, 11, 17, 17)
            edged = cv2.Canny(gray, 30, 200)
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
            detected = 0 if screenCnt is None else 1
            if detected == 0:
                continue
            if detected == 1:
                cv2.drawContours(image, [screenCnt], -1, (0, 255, 0), 3)
            mask = np.zeros(gray.shape, np.uint8)
            new_image = cv2.drawContours(mask, [screenCnt], 0, 255, -1,)
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

    # Getting the longitude and latitude values
    while 0 == GPS.read():
        if not (gps.MODE_SET & GPS.valid):
            continue
        if((gps.isfinite(GPS.fix.latitude)) and (gps.isfinite(GPS.fix.longitude))):
            lat = GPS.fix.latitude
            lon = GPS.fix.longitude
            break

    # after finish
    # Set environment variables for your credentials
    account_sid = ""
    auth_token = ""
    client = Client(account_sid, auth_token)
    nomin = Nominatim(user_agent="GetLoc")
    address = nomin.reverse("{},{}".format(lat, lon))

    message = client.messages.create(
    body=("We found a {} {} with license plate {} at:\n\n {}\n\nLatitude: {:.6f}\nLongitude: {:.6f}"
          .format(color, type, license, address.address, lon, lat)),
    from_="+18775255017",
    to="+14404977348")# this will be a designated authority number
