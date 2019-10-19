from darknet import Darknet
from qr import QR 
from sticker import Sticker
from picamera.array import PiRGBArray
from picamera import PiCamera
from time import sleep
import cv2
from concurrent.futures import ThreadPoolExecutor
from text_to_speech import TTS

camera = PiCamera()
sticker = Sticker()
darknet = Darknet()
qr = QR()
tts = TTS()

iter = 1
while True:
    rawCapture = PiRGBArray(camera)
    camera.capture(rawCapture, format="bgr")
    image = rawCapture.array
    with ThreadPoolExecutor() as executor:
        p_darknet = executor.submit(darknet.detect, image)
        p_sticker = executor.submit(sticker.find_sticker, image)
        p_qr = executor.submit(qr.scan, image)
        print("{} Darknet:".format(iter))
        print(p_darknet.result()[0])
        for name, _, _ in p_darknet.result()[0]:
            tts.play_audio(name)
        print("{} Sticker:".format(iter))
        print(p_sticker.result())
        if p_sticker.result()[0]:
            tts.play_audio("Sticker Found")
        print("{} QR:".format(iter))
        for x, y, data in p_qr.result():
            print(x, y, data)
            tts.play_audio(data)
        iter += 1