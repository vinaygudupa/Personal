#!/bin/bash
#
# Accepts arg of pcap file w/only 2 RTP streams
# Creates a .<raw>, .<txt> file and a .wav file
# Current codec support: PCMA and PCMU

# check for -h -help or --help

if [[ $1 == "-h" || $1 == "-help" || $1 == "--help" || $1 == "" ]]
then
    cat <<EOF

pcap2wav_using_rtpbreak is a simple utility to make it easier to extract the audio from a pcap

Dependencies:
   apt-get install -y tshark sox

Usage:

  pcap2wav_using_rtpbreak [opts] filename.pcap <target filename> <MS_mode src/dst> <MS_PVT_IP>

Script attempts to create a few files: a .<raw>, .<txt> file and a .wav file for each RTP stream

Supported codecs:
 PCMU (G711 ulaw)
 PCMA (G711 Alaw)

Supported options:
 -z  Perform "clean and zip" - After converting to wav files the program will "clean up"
                               by putting the wav files into a .tgz file and then removing
                               the .wav and .<raw>, .<txt> files from the disk.
EOF

exit
fi

if [[ $1 == "-z" ]]
then
    CLEAN=true
    CAPFILE=$2
    TARGETFILE=$3
    MODE=$4
    IP=$5
else
    CLEAN=false
    CAPFILE=$1
    TARGETFILE=$2
    MODE=$3
    IP=$4
fi

RTPBREAK=`which rtpbreak`
SOX=`which sox`

if [[ $RTPBREAK == "" ]]
then
    echo "rtpbreak not found. Please install rtpbreak and then re-run this script"
    exit
fi

if [[ $SOX == "" ]]
then
    echo "sox not found. Please install Sox and then re-run this script"
    exit
fi

# Make sure pcap exists
if [ -f $CAPFILE ]
then
    echo "Found $CAPFILE, working..."
else
    echo "$CAPFILE not found, exiting."
    exit
fi

# Set target file names; default is "pcap2wav.<codec>" and "pcap2wav.wav"
if [[ $TARGETFILE == "" ]]
then
    echo "target file $TARGETFILE not specified, using capfile "
    TARGETFILE=$CAPFILE
    #exit
else
    echo "Using $TARGETFILE"
fi

echo "Creating RTP streams from $CAPFILE..."

#$RTPBREAK -W -f -g -p "dst host 23.29.23.42" -d . -r $CAPFILE 
$RTPBREAK -W -f -g -p "$MODE host $IP" -d . -r $CAPFILE 

# Create wav files from rtpstreams
$SOX -r8000 -c1 -t ul rtp.0.0.raw -t wav ${TARGETFILE}_0.wav
#$SOX -r8000 -c1 -t ul rtp.0.1.raw -t wav ${TARGETFILE}_1.wav

# If two streams then assume they're a pair and combine them nicely

echo "Combining 2 streams into a single wav file for convenience"
# Find shorter recording, calc time diff in samples
samples1=`soxi -s ${TARGETFILE}_0.wav`
samples2=`soxi -s ${TARGETFILE}_1.wav`

if [[ $samples1 -gt $samples2 ]]
then
    longer="${TARGETFILE}_0.wav"
    shorter="${TARGETFILE}_1.wav"
    delay=`expr $samples1 - $samples2`
else
    longer="${TARGETFILE}_1.wav"
    shorter="${TARGETFILE}_0.wav"
    delay=`expr $samples2 - $samples1`
fi

pad="${delay}s"
command="$SOX $shorter ${TARGETFILE}_tmp.wav pad $pad 0s"
$command

# Create "combined" file, padding beginning with silence
command="$SOX -m ${TARGETFILE}_tmp.wav $longer ${TARGETFILE}_mixed.wav"
$command
rm -fr ${TARGETFILE}_tmp.wav

if [[ $CLEAN == "true" ]]
then
    echo "Clean option"
    ZIPFILE=${TARGETFILE}.tgz
    rm -fr $ZIPFILE
    /bin/tar czf $ZIPFILE ${TARGETFILE}_*.wav > /dev/null 2>& 1
    rm -fr $TARGETFILE.tmp
    rm -fr ${TARGETFILE}_*.wav
    rm rtp.0*
else
    echo "No clean option specified - leaving .<codec> and .wav files on system."
fi

echo
echo "Operation complete"
echo
