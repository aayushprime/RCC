# How to add watermarks to vidoes using ffmpeg?
`ffmpeg -i sing.mp4 -c:v libvpx -i w.webm -c:v libvpx -stream_loop -1 -i wl.webm  -filter_complex "[0][1]overlay=x=20:y=90:eof_action=pass[a];[2]setpts=PTS+9/TB[b];[a][b]overlay=x=10:y=10:shortest=1"  out.mp4 -y`

-i : for input file(photo or video)
-c:v : specify codec (what type of file, libvpx is for webm type, to read webm transparency)
-filter_complex : A program in itself that does stuff to the input or generated streams!
-stream_loop -1 : Loop the following input stream (-1: infinite) times before ending

# Complex filter syntax
filters are separated by a semicolon
Something like this "filter; filter; filter"
anything that begins with "a" is an audio filter. `ffmpeg -filters` for more info.
Then overlay is a filter that takes 2 streams [1] and [2] (from input streams) and overlays one on other 
to give filters parameters use: "filtername=parametername=value:another_parametername:value"
x and y are parameters for the position on which to begin the overlayed video!
shortest=1 means end the stream when the shorter video runs out!
eof_action=pass[a]
Defines what to do when the stream runs out: pass means remove any trace of the stream that ran out, default is to extend the last frame of the stream

setpts filter changes the speed/adds delays to a stream
Add 9 second delay to [2] and output it as stream [b]
T and B are special variables that are used by the setpts filter
[2]setpts=PTS+9/TB[b];




