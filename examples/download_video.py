from goprocam import GoProCamera, constants
import time
gpCam = GoProCamera.GoPro()

videos_duration=[10,30,60,120,180]
gpCam.video_settings("1080p","60")
gpCam.gpControlSet(constants.Video.PROTUNE_VIDEO, constants.Video.ProTune.ON)
for i in videos_duration:
	print("Recording " + str(i) + " seconds video")
	gpCam.downloadLastMedia(gpCam.shoot_video(i), custom_filename="VIDEO_"+str(i)+".MP4")
	time.sleep(2)
	