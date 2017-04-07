
VBR="2500k"
FPS="30"
QUAL="medium"
URL="rtmp://rtmp-api.facebook.com:80/rtmp"

SOURCE="udp://127.0.0.1:10000"
KEY="YOUR_FB_API_KEY"

ffmpeg \
    -i "$SOURCE" -deinterlace \
    -vcodec libx264 -pix_fmt yuv420p -preset $QUAL -r $FPS -g $(($FPS * 2)) -b:v $VBR \
    -acodec libmp3lame -ar 44100 -threads 6 -qscale 3 -b:a 712000 -bufsize 512k \
-f flv "$URL/$KEY"
