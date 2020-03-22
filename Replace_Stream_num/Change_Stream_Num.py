from scapy.all import *

if len(sys.argv) != 4:
	print("Usage : python3 Change_Stream_Num.py <pcap_file_full_path> <src_port of RTP stream of which Stream num needs to be changed> <New stream num>")
else:
	data = rdpcap(sys.argv[1])
	for pkt in data:
		if pkt['UDP'].sport == int(sys.argv[2]):
			pkt[Raw].load = pkt[Raw].load.replace(b'\xa0N\x83', b'\xa0N\x84')

	wrpcap("PCMU_3_30.pcap", data)
