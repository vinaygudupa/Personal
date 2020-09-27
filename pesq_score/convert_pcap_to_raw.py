from scapy.all import *
import sys

if len(sys.argv) != 4:
    print("Usage : python3 Pcap_to_Raw.py <pcap_file_full_path> <output_file_name> <Jitter buffer in ms>")
else:
    raw_file = open(sys.argv[2],'wb')
    data = rdpcap(sys.argv[1])
    time_stamp_old = data[0].time
    flag = 1
    for pkt in data:
        if flag == 0:
            new_time = pkt.time
            time_diff = new_time - old_time
            old_time = new_time
            time_diff_in_ms = time_diff * 1000
            if int(time_diff_in_ms) > int(sys.argv[3]):
                print(time_diff_in_ms)
                pkts_to_write_blank_data = int(time_diff_in_ms/20)
                try:
                    blank_data = b''
                    for i in range(pkts_to_write_blank_data):
                        blank_data += 170 * b'\xff'
                    raw_file.write(blank_data)
                except Exception as e:
                    print("Exception: " + str(e))
        else:
            old_time = pkt.time
            flag = 0
        rtp_data = pkt['Raw'].load
        rtp_payload = rtp_data[12:]
        raw_file.write(rtp_payload)
    raw_file.close()
    print(sys.argv[2] + " Raw file generated")
