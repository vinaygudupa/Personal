#!/bin/sh
#Scenarios to simulate call flow
SCENARIO_FILE=/home/ubuntu/Vinay_Test/PESQ/
#media server IP or Remote sending address
MS_IP=phone-qa.voice.plivodev.com
LOCAL_PORT=`python -c 'import socket; s=socket.socket(); s.bind(("", 0)); print(s.getsockname()[1]); s.close()'`
LOCAL_CONTROL_PORT=`python -c 'import socket; s=socket.socket(); s.bind(("", 0)); print(s.getsockname()[1]); s.close()'`
LOCAL_MEDIA_PORT=`python -c 'import socket; s=socket.socket(); s.bind(("", 0)); print(s.getsockname()[1]); s.close()'`
SFT_EXE=/home/ubuntu/sipp
FULL_PATH1=$SCENARIO_FILE$1
#echo "$FULLPATH"
#echo "$FULLPATH2"
##########with sipp log############
if [ "$1" != "" ] ; then
    sudo $SFT_EXE -sf $FULL_PATH1 -p $LOCAL_PORT -mp $LOCAL_MEDIA_PORT -cp $LOCAL_CONTROL_PORT $MS_IP -m 1 -r 1 -aa -timeout 60s 
else
    echo "Usage:./uac_number.shInvite_xml_filename"
    exit 1
fi
