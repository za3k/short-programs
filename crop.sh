dirname=$(dirname "$1")
filename=$(basename "$1")
extension="${filename##*.}"
if [ "${extension,,}" != "jpg" ]; then
    echo "Not a jpg file"
    exit 1
fi
cropgui "$1"
filename="${filename%.*}"
renamed="${filename}-crop.${extension}"
renamed="${renamed,,}"
if [ -e "$dirname/$renamed" ]
then
    mv -f "$dirname/$renamed" "$1"
fi
