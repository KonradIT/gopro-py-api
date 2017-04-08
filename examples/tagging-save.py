from goprocam import GoProCamera, constants
import json
gpCam = GoProCamera.GoPro(constants.gpcontrol)

## This script will download videos from the camera that have hilight tags in them and create a json file containing the tag location in milliseconds with each video 
media = gpCam.listMedia(True, True)
for i in media:
	folder= i[0]
	filename = i[1]
	if filename.endswith('MP4'):
		tags_in_video=gpCam.getVideoInfo("tags", filename, folder)
		if not tags_in_video == []:
			gpCam.downloadMedia(folder,filename)
			filename_tags=filename.replace('MP4','json')
			hs = open(filename_tags,"a")
			hs.write(str(tags_in_video))
			hs.close() 