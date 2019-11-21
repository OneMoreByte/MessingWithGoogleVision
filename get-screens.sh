#!/bin/bash

NAME=0
IFS=$'\n'
mkdir -p ./src
for VIDEO in $(find . -name '*.mkv' -print); do
    echo $VIDEO
    TIME=$(ffprobe -i $VIDEO -show_entries format=duration -v quiet -of csv="p=0")
    MAXTIME=${TIME/.*}
    RAND=$(od -A n -t d -N 3 /dev/urandom)
    SEC=$(($RAND % $MAXTIME))
#    echo $SEC
    ffmpeg -ss "$SEC" -i $VIDEO -frames:v 1 -f image2 "./src/$NAME.jpg"
    NAME=$((NAME+1))

done
