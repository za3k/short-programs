#!/bin/bash
if [ -n "$1" ]
then
    FILE="$1"; shift
else
   "Supply a filename to $0"
   exit 1
fi
TAG="$(find -type d -printf '%f\n' | dmenu -p "Select a tag for the file")"
echo "file is $FILE"
echo "tag is $TAG"
if [ ! -e "$TAG" ]
then
    mkdir "$TAG"
fi

if [ -d "$TAG" ]
then
    mv "$FILE" "$TAG"
else
    echo "$TAG is not a directory/tag" >/dev/stderr
    exit 1
fi

