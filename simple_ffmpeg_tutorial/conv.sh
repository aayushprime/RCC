#!/bin/bash
# ffmpeg -i sing.mp4 -c:v libvpx -i w.webm -filter_complex "[0][1]overlay=x=20:y=90[a];movie=w.webm:loop=0,setpts=N/FRAME_RATE/TB[b],[a][b]overlay=x=10:y=10:shortest=1"  out.mp4 -y
# ffmpeg -i sing.mp4 -c:v libvpx -i w.webm -filter_complex "[0][1]overlay=x=20:y=90[a];movie=wl.webm:loop=0,setpts=N/FRAME_RATE/TB[b],[a][b]overlay=x=10:y=10:shortest=1"  out.mp4 -y
# ffmpeg -i sing.mp4 -c:v libvpx -i w.webm -c:v libvpx -i wl.webm -filter_complex "[0][1]overlay=x=20:y=90[a];[2]loop=-1:-1:0[b];[a][b]overlay=x=10:y=10:shortest=1"  out.mp4 -y
ffmpeg -i sing.mp4 -c:v libvpx -i w.webm -c:v libvpx -stream_loop -1 -i wl.webm  -filter_complex "[0][1]overlay=x=20:y=90:eof_action=pass[a];[2]setpts=PTS+9/TB[b];[a][b]overlay=x=10:y=10:shortest=1"  out.mp4 -y

