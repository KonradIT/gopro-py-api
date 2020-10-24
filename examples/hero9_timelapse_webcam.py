import sys
import time
from goprocam import GoProCamera, constants
import threading
import logging

"""
I use PM2 to start my GoPro cameras, using a Raspberry Pi 4, works perfectly.

pm2 start timelapse.py --cron "30 7 * * *" --log timelapse.log --no-autorestart

This script will overrride some settings for reliability:

Voice control: OFF
AutoPower off: NEVER
Beeps: OFF (Do not want the camera beeping at 6AM)

NightLapse configuration left untouched, I recommend always using Auto shutter for sunrise and locking the White Balance to 4000k or higher.
"""


def start_timelapse(interface):
    gopro = GoProCamera.GoPro(ip_address=GoProCamera.GoPro.getWebcamIP(
        interface), camera=constants.gpcontrol, webcam_device=interface)
    logging.info(
        "Started goprocam instance with interface {}".format(interface))
    gopro.gpControlSet(constants.Setup.VOICE_CONTROL,
                       constants.Setup.VoiceControl.OFF)
    gopro.gpControlSet(constants.Setup.AUTO_OFF, constants.Setup.AutoOff.Never)
    logging.info("All config set")
    gopro.mode(constants.Mode.MultiShotMode,
               constants.Mode.SubMode.MultiShot.NightLapse)
    gopro.shutter(constants.start)
    logging.info("Started timelapse")


cameras = sys.argv[1]
cameras = cameras.split(",")

for interface in cameras:
    thr = threading.Thread(target=start_timelapse, args=(interface,))
    thr.start()
