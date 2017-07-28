from goprocam import GoProCamera, constants
gopro = GoProCamera.GoPro()

## Downloads the video between 2 hilight tags
last_media = gopro.getMedia()
if last_media.endswith(".MP4"):
	folder = gopro.getMediaInfo("folder")
	file = gopro.getMediaInfo("file")
	number_of_tags = gopro.getVideoInfo("tag_count",file,folder)
	if number_of_tags != 0 and number_of_tags % 2 == 0:
		#Even number of tags
		tags = gopro.getVideoInfo("tags",file,folder)
		print(tags)
		status_id = gopro.getClip(folder + "/" + file, constants.Clip.R720p, constants.Clip.FPS_NORMAL, str(tags[0]), str(tags[1]))		
		url = gopro.clipStatus(str(status_id))
		while gopro.getClipURL(str(status_id)) == None:
			gopro.getClipURL(str(status_id))
		print(gopro.getClipURL(str(status_id)))
		gopro.downloadLastMedia(path=gopro.getClipURL(str(status_id)), custom_filename = gopro.getInfoFromURL(gopro.getClipURL(str(status_id)))[1])
		print("Downloaded.")