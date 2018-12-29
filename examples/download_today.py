from goprocam import GoProCamera, constants
import argparse
import datetime

parser = argparse.ArgumentParser()
parser.add_argument('--video', "-v", help='Download videos only', required=False, type=bool)
parser.add_argument('--photo', "-p", help='Download photos only', required=False, type=bool)
parser.add_argument('--all', "-a", help='Download all', required=False, type=bool)
parser.add_argument('--out', "-o", help='Output path', default="")

args = parser.parse_args()
gopro = GoProCamera.GoPro()

medialist = gopro.listMedia(format=True, media_array=True)
currentdate = datetime.datetime.today().date()

if args.video:
	for media in medialist:
		dat = datetime.datetime.fromtimestamp(int(media[3])).date()
		if "MP4" in media[1] and dat == currentdate:
			newpath = args.out + "/" + media[1]
			gopro.downloadMedia(media[0], media[1], newpath)
if args.photo:
	for media in medialist:
		dat = datetime.datetime.fromtimestamp(int(media[3])).date()
		if "JPG" in media[1] and dat == currentdate:
			newpath = args.out + "/" + media[1]
			gopro.downloadMedia(media[0], media[1], newpath)
if args.all:
	for media in medialist:
		dat = datetime.datetime.fromtimestamp(int(media[3])).date()
		if dat == currentdate:
			newpath = args.out + "/" + media[1]
			gopro.downloadMedia(media[0], media[1], newpath)

	
