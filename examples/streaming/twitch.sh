VBR="2500k"
FPS="30"
QUAL="medium"
URL="rtmp://live-fra.twitch.tv/app"

SOURCE="udp://127.0.0.1:10000"
KEY="YOUR_API_KEY_HERE"

ffmpeg \
    -i "$SOURCE" -deinterlace \
    -vcodec libx264 -pix_fmt yuv420p -preset $QUAL -r $FPS -g $(($FPS * 2)) -b:v $VBR \
    -acodec libmp3lame -ar 44100 -threads 6 -qscale 3 -b:a 712000 -bufsize 512k \
-f flv "$URL/$KEY"
