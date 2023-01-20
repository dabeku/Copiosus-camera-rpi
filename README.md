## Streams the camera to Copiosus-viewer

```
python3 main.py -platform=mac -cmd=start -cam="FaceTime HD Camera" -width=960 -height=480 -framerate=30
python3 main.py --width=640 --height=480 --framerate=30
```

This script is intened to work on Bullseye OS of RPi.

It will call

```
libcamera-vid -t 0 --codec libav --libav-format mpegts  -o "udp://<ip-addr>:<port>"
```

after Copiosus-viewer connect to the RPi.

## Testing

```
ffmpeg -f avfoundation -framerate 30 -i "0" out.mpg
ffplay udp://192.168.178.46:8554 -vf "setpts=N/30" -fflags nobuffer -flags low_delay -framedrop
ffmpeg -f avfoundation -framerate 30 -i "0" -f mpegtsv  udp://192.168.178.46:6201
ffmpeg -f avfoundation -framerate 30 -video_size 640x480 -flags:v +global_header -i "0" -f mpegts udp://192.168.178.46:6201
```