#!/bin/bash

NETWORK=outpost

usage(){
    echo "Usage: internet.sh MINUTES REASON"
}

case "$#" in
    2)
    echo "$(date) ($1 minutes): $2" >> ~/.internet_reasons
    trap "sudo netcfg -d $NETWORK;exit" INT TERM EXIT
    if retry "sudo netcfg $NETWORK"
    then
        sleep $(( 60 * $1 ))
    fi
    ;;
    *)
    usage
    ;;
esac
