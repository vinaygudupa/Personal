### Python 2.7 Script by Neil Bernard neil@themoog.org
## This script is for editing RTP header information in PCAP files to manipulate RTP timestamp and SSRC
## for testing hardware transport stream devices and testing SMPTE 2022-2 handling

## There is some error checking for scapy network layers but try to keep capture as clean as possible
## also try to keep captures under 260Mb for performance, can take a good 20mins on an intel i7 / 16GB ram

#### Basic Scapy Tutorial

# *https://www.youtube.com/watch?v=ADDYo6CgeQY

#### Scapy cheat sheet

# https://blogs.sans.org/pen-testing/files/2016/04/ScapyCheatSheet_v0.2.pdf

#### Scapy RTP Library https://fossies.org/linux/scapy/scapy/layers/rtp.py

# import scapy
from scapy.all import rdpcap
from scapy.all import wrpcap
from scapy.all import RTP
from scapy.all import *

infile = "test_rtp.pcap"
outfile = "modified_" + infile
dest_port = 2000 # usefull to make sure you only action packets that are RTP

# load packet capture
print "Loading Packet Capture Keep <200Mb - Might take a few mins....."
pl = rdpcap(infile)
print "Loading complete!"

# print number of packets
print(len(pl))
# # print rtp timestamp
# print(RTP(pl[0][UDP].payload).timestamp)
numberofpckts = len(pl)

print numberofpckts

for pkt in range(numberofpckts):

    # You cant use the [RTP] layer on a list index so you have to put it in a
    # variable first. Also need to make sure its a UDP packet with .haslayer(UDP):
    # https://stackoverflow.com/questions/48763072/scapy-getting-trailer-field-in-the-dissector

    if pl[pkt].haslayer(UDP):
        packet = pl[pkt][UDP]

    else:
        print "Probably Not a UDP / RTP Packet# {0}".format(pkt)


    # You need to do the line below to force RTP detection and manipulation
    # https://stackoverflow.com/questions/44724186/decode-rtp-over-udp-with-scapy

    if pl[pkt].haslayer(UDP):
        if packet["UDP"].dport==2000: # Make sure its actually RTP
            packet["UDP"].payload = RTP(packet["Raw"].load)

        #### un-commment and change lines below to manipulate headers

            # packet[RTP].version = 0
            # packet[RTP].padding = 0
            # packet[RTP].extension = 0
            # packet[RTP].numsync = 0
            # packet[RTP].marker = 0
            # packet[RTP].payload_type = 0
            # packet[RTP].sequence = 0

            # packet[RTP].timestamp = 0

            packet[RTP].sourcesync = 0
            # packet[RTP].sync = 0

            ### Calculate UDP Checksum or they will now be wrong!

            #https://scapy.readthedocs.io/en/latest/functions.html

            checksum_scapy_original = packet[UDP].chksum

            # set up and calculate some stuff

            packet[UDP].chksum = None ## Need to set chksum to None before starting recalc
            packetchk = IP(raw(packet))  # Build packet (automatically done when sending)
            checksum_scapy = packet[UDP].chksum
            packet_raw = raw(packetchk)
            udp_raw = packet_raw[20:]
            # in4_chksum is used to automatically build a pseudo-header
            chksum = in4_chksum(socket.IPPROTO_UDP, packetchk[IP], udp_raw)  # For more infos, call "help(in4_chksum)"

            # Set the new checksum in the packet

            packet[UDP].chksum = checksum_scapy # <<<< Make sure you use the variable in checksum_scapy

            # needed below to test layers before printing newts/newsourcesync etc to console

            if pl[pkt].haslayer(UDP):
                newts = RTP(pl[pkt][UDP].payload).timestamp
                newsourcesync = RTP(pl[pkt][UDP].payload).sourcesync

            else:
                newts = 999
                newsourcesync = 999

            print("Changing packet {0} of {3} to new timestamp {1} SSRC {2} Old UDP chksum {4} >> New UDP chksum ???").format(pkt+1,newts,newsourcesync,numberofpckts,hex(checksum_scapy_original))

        else:
            print "Probably Not a UDP / RTP Packet# {0}".format(pkt)

# Write out new capture file
wrpcap(outfile, pl)