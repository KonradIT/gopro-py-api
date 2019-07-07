import time
import numpy as np
from goprocam import GoProCamera, constants
gpCam = GoProCamera.GoPro()

# Extracts clips from latest video

latestVideo = gpCam.getVideoInfo()
print("Tag count %s" % latestVideo.get(constants.Info.TagCount))
arrayLength = latestVideo[constants.Info.TagCount]
if arrayLength % 2 == 0:
    print("Matching tag pairs!")
    splitArray = np.array_split(
        latestVideo[constants.Info.Tags], arrayLength/2)
    for tag in splitArray:
        startMs = tag[0]
        stopMs = tag[1]
        print("\n[START ms] %s\n[STOP  ms] %s" %
              (startMs, stopMs))
        fileName = "%s/%s" % (gpCam.getMediaInfo("folder"),
                              gpCam.getMediaInfo("file"))
        videoId = gpCam.getClip(fileName, constants.Clip.R1080p,
                                constants.Clip.FPS_NORMAL, str(startMs), str(stopMs))
        print("On queue!\nVideo Id: %s\nStatus: %s" %
              (videoId, gpCam.clipStatus(str(videoId))))
        time.sleep(1)
        while(gpCam.clipStatus(str(videoId)) != "complete"):
            time.sleep(1)
        time.sleep(2)
        print("Downloading!\nVideo Id: %s\nStatus: %s" %
              (videoId, gpCam.clipStatus(str(videoId))))
        url = gpCam.getClipURL(str(videoId))
        download = [
            url.split("/")[len(url.split("/"))-1],
            url.split("/")[len(url.split("/"))-2]]
        print("Downloading %s" % download)
        try:
            gpCam.downloadLastMedia(
                path=url, custom_filename="output/%s_%s_%s" % (startMs, stopMs, download[0].replace("TRV", "MP4")))
        except(Exception) as e:
            time.sleep(2)
            gpCam.downloadLastMedia(
                path=url, custom_filename="output/%s_%s_%s" % (startMs, stopMs, download[0].replace("TRV", "MP4")))
