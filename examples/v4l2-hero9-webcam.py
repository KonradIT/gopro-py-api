import sys
from goprocam import GoProCamera, constants
import ffmpeg

print("Run modprobe v4l2loopback device=1 video_nr=44 card_label=\"GoPro\" exclusive_caps=1")
input("Hit enter when done!")
gopro = GoProCamera.GoPro(ip_address=GoProCamera.GoPro.getWebcamIP(
    sys.argv[1]), camera=constants.gpcontrol, webcam_device=sys.argv[1])
gopro.webcamFOV(constants.Webcam.FOV.Wide)
gopro.startWebcam()
udp_stream = "udp://{}:8554".format(GoProCamera.GoPro.getWebcamIP(sys.argv[1]))
stream = ffmpeg.input(udp_stream, vsync=2, fflags="nobuffer",
                      flags="low_delay", probesize=3072)
stream = ffmpeg.output(stream, "/dev/video44",
                       ar="44100", vcodec='rawvideo', pix_fmt="yuv420p", format="v4l2")
ffmpeg.run(stream)


# "ExecStart=/usr/bin/ffmpeg -vsync 2 -fflags nobuffer -flags low_delay -probesize 3072 -nostdin -i udp://172.26.169.51:8554 -ar 44100 -f v4l2 -pix_fmt yuv420p -vcodec rawvideo /dev/video44"
# Thanks to https://gist.github.com/andrewhowdencom/b7ed844ceb6fc44226974723abc7b2d1
# https://twitter.com/andrewhowdencom/status/1309153832350486529
