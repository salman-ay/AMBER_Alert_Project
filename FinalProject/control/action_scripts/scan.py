from threading import Thread
from time import sleep
from twilio.rest import Client

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

def threadFunction(info):
    # the scanning function goes here
    # while(STATUS == "on"):
    sleep(10)
    STATUS = "off"
    # after finish
    # Set environment variables for your credentials (am lazy c:)
    # Read more at http://twil.io/secure
    account_sid = "ACee2fd0f1586d4ca13f67e265e50a58a5"
    auth_token = "f3603044422224d92baa45f4bfc4887a"
    client = Client(account_sid, auth_token)
    message = client.messages.create(
    body="We found the {} {} vehical with license plate {} at: {}"
        .format(info[1], info[0], info[2], "CWRU"),# location will be taken from GPS 
    from_="+18775255017",
    to="+14404977348")# this will be a designated authority number
