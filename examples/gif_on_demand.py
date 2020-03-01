from glitch_this import ImageGlitcher
from goprocam import GoProCamera, constants
import tweepy
import time
import logging
from wifi import Cell, Scheme
import os
import cv2
import numpy as np

keys = dict(
    TWITTER_CONSUMER_KEY="...",
    TWITTER_CONSUMER_SECRET="...",
    TWITTER_ACCESS_TOKEN="...",
    TWITTER_ACCESS_TOKEN_SECRET="...",
    GOPRO_SSID="...",
    GOPRO_PASSWORD="...",
    HOME_SSID="...",
    HOME_PASSWORD="..."
)


glitcher = ImageGlitcher()
os.system(
    "nmcli dev wifi connect " + keys["GOPRO_SSID"] + " password " + keys["GOPRO_PASSWORD"])
time.sleep(2)
gopro = GoProCamera.GoPro()

auth = tweepy.OAuthHandler(
    keys['TWITTER_CONSUMER_KEY'], keys['TWITTER_CONSUMER_SECRET'])
auth.set_access_token(
    keys['TWITTER_ACCESS_TOKEN'], keys['TWITTER_ACCESS_TOKEN_SECRET'])
api = tweepy.API(auth)


while True:
    if input(">>> ") == "s":
        gopro.take_photo(1)
        print("Downloading!")
        # Download picture
        gopro.downloadLastMedia(custom_filename="tmp.jpg")
        glitch_img = glitcher.glitch_image(
            "tmp.jpg", 3, 4, 5, True, True, False, 1, 4)
        glitch_img.save('glitched_test.png')

        os.system("nmcli dev wifi connect " +
                  keys["HOME_SSID"] + " password " + keys["HOME_PASSWORD"])

        img = cv2.imread('glitched_test.png')
        res = cv2.resize(img, dsize=(800, 600),
                         interpolation=cv2.INTER_CUBIC)
        cv2.imwrite("to_twitter.png", res)
        api.update_with_media('to_twitter.png')
        os.system(
            "nmcli dev wifi connect " + keys["GOPRO_SSID"] + " password " + keys["GOPRO_PASSWORD"])
        time.sleep(2)
