#!/usr/bin/env bash

input='./twitter_demo.mkv'
output="${input%.*}.gif"
fps=15

mkdir -p frames
ffmpeg -loglevel warning -stats -i "${input}" -r ${fps} frames/%04d.png
convert -delay $(( 100 / fps )) -loop 0 -layers optimize -fuzz 10% frames/*.png "${output}"
rm -r frames

