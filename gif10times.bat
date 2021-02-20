@echo off
setlocal enabledelayedexpansion
cd %~dp0

ffmpeg -i input.gif  -movflags faststart -pix_fmt yuv420p -vf "scale=trunc(iw/2)*2:trunc(ih/2)*2" -r 60 output.mp4
ffmpeg -i output.mp4 -vf setpts=PTS/5.0 -af atempo=5.0 -q 0 -r 60 output_10.mp4
ffmpeg -i output_10.mp4 -vf "palettegen" -y palette.png
ffmpeg -i output_10.mp4 -i palette.png -lavfi "fps=60,scale=640:-1:flags=lanczos [x]; [x][1:v] paletteuse=dither=bayer:bayer_scale=5:diff_mode=rectangle" -q 0 -r 60 -y output.gif