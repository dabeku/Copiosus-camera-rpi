## Streams the camera to Copiosus-viewer

```
python3 main.py
```

This script is intened to work on Bullseye OS of RPi.

It will call

```
libcamera-vid -t 0 --codec libav --libav-format mpegts  -o "udp://<ip-addr>:<port>"
```

after Copiosus-viewer connect to the RPi.
