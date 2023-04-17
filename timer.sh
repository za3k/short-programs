#!/bin/bash
START=$(date +%s)

if [ $# -ne 1 ]
then
    echo 'Usage: timer <minutes>'
    exit 1
fi

SECONDS=$((60 * $1))
END=$(($START + $SECONDS))
unset SECONDS

watch -n1 -t "time_diff $END \`date +%s\`"
