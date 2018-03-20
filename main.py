import cv2
from multiprocessing import Process
#from gtts import gTTS
import time
from webcam import Webcam
from PIL import Image
from pytesseract import image_to_string
from MarkNplay import MarkNplay
import pyttsx3
#import os
def main():
    webcam = Webcam()
    webcam.start()
    mnp = MarkNplay()

    while True:
        image = webcam.get_current_frame()
        mnp.screen_thread(image)

        cv2.imshow('AR Book Reader', image)
        cv2.waitKey(10)


def Text():
    a = image_to_string(Image.open('/home/sam/Desktop/hack/test.jpg'), lang='eng')
    engine = pyttsx3.init()
    time.sleep(10)
    rate = engine.getProperty('rate')
    engine.setProperty('rate', rate - 70)
    engine.say(a)
    #myobj = gTTS(text=a, lang='en', slow=False)
    #myobj.save("welcome.mp3")
    engine.runAndWait()



if __name__ == '__main__':
    p1 = Process(target=main)
    p1.start()
    p2 = Process(target=Text)
    p2.start()




