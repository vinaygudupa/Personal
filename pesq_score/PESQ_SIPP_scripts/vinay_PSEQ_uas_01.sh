#!/bin/sh
#Scenarios to simulate call flow
SCENARIO_FILE=/home/ubuntu/Vinay_Test/PESQ/
#media server IP or Remote sending address
MS_IP=phone-qa.voice.plivodev.com
LOCAL_PORT=`python -c 'import socket; s=socket.socket(); s.bind(("", 0)); print(s.getsockname()[1]); s.close()'`
LOCAL_CONTROL_PORT=`python -c 'import socket; s=socket.socket(); s.bind(("", 0)); print(s.getsockname()[1]); s.close()'`
MEDIA_CONTROL_PORT=`python -c 'import socket; s=socket.socket(); s.bind(("", 0)); print(s.getsockname()[1]); s.close()'`
SFT_EXE=/home/ubuntu/sipp
FULL_PATH=$SCENARIO_FILE$1
FULL_PATH2=$SCENARIO_FILE$2
#echo "$FULLPATH"
#echo "$FULLPATH2"
##########with sipp log############
if [ "$1" != "" ] && [ "$2" != "" ]; then
    sudo $SFT_EXE -sf $FULL_PATH -p $LOCAL_PORT -cp $LOCAL_CONTROL_PORT $MS_IP -m 1 -aa
    if test $? -eq 0
    	then
        	echo Test $i failed 
    		sudo $SFT_EXE -sf $FULL_PATH2 -p $LOCAL_PORT -mp $MEDIA_CONTROL_PORT -cp $LOCAL_CONTROL_PORT $MS_IP -m 1 -aa -timeout 60s 
    	else
        	exit 1
    fi 
else
    echo "Usage:./uas_number.sh register_xml_filename Invite_xml_filename"
    exit 1
fi
