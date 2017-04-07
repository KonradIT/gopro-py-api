from goprocam import GoProCamera, constants
import json
gpCam = GoProCamera.GoPro(constants.gpcontrol)

## This script will download videos from the camera that have hilight tags in them and create a json file containing the tag location in milliseconds with each video 
json_media = gpCam.listMedia()
json_parse = json.loads(json_media)
for i in json_parse['media']:
	folder = i['d']
	for i2 in i['fs']:
		filename = i2['n']
		if filename.endswith('MP4'):
			tags_in_video=gpCam.getVideoInfo("tags", filename, folder)
			if not tags_in_video == []:
				gpCam.downloadMedia(folder,filename)
				filename_tags=filename.replace('MP4','json')
				hs = open(filename_tags,"a")
				hs.write(str(tags_in_video))
				hs.close() 