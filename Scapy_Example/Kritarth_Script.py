#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re, sys
from random import seed
from random import randint
from scapy.all import *
from scapy.utils import PcapWriter
seed(1)


def repl(m):
    return b'X-Header:' + b'*' * (len(m.group())-11) + b'\r\n'
ip_map = {}


def generate_fake_ip(ip):
    if ip in ip_map:
        return ip_map[ip]
    new_ip_parts = [ip.split('.')[0]]
    for p in ip.split('.')[1:]:
        if len(p) == 1:
            new_ip_parts.append(str(randint(0, 9)))
        elif len(p) == 2:
            new_ip_parts.append(str(randint(10, 99)))
        elif len(p) == 3:
            new_ip_parts.append(str(randint(100, 255)))
    ip_map[ip] = '.'.join(new_ip_parts)
    return ip_map[ip]
    
    
    
def modify_pcap(pcapfile):
    packets = rdpcap(pcapfile)
    # and modify each packet
    for p in packets:
        p[Raw].load = p[Raw].load.replace(b"+18668604259", b"+11111111111")
        p[Raw].load = p[Raw].load.replace(b"+14696388545", b"+10000000000")
        p[Raw].load = p[Raw].load.replace(b"+12085955367", b"+10000000000")
        p[Raw].load = p[Raw].load.replace(b"+14696388492", b"+10000000000")
        p[Raw].load = re.sub(b"X-[a-zA-Z0-9-]+: [^\r\n]*\r\n", repl, p[Raw].load)
        p[Raw].load = re.sub(b"sip:s[0-9].opensips-outbound.plivops.com", b"sip:outbound-server.xyzxyzxyzxyz.com", p[Raw].load)
        if p[UDP].len == 180 and (p[UDP].dport in (29818, 17516, 20390) or p[UDP].sport in (29818, 17516, 20390)):
            p[Raw].load = p[Raw].load[:-160] + bytes([255]) * 160
        # replace ips
        src = p[IP].src
        dst = p[IP].dst
        p[IP].src = generate_fake_ip(src)
        p[IP].dst = generate_fake_ip(dst)
        p[Raw].load = p[Raw].load.replace(src.encode(), p[IP].src.encode())
        p[Raw].load = p[Raw].load.replace(dst.encode(), p[IP].dst.encode())
        p[Raw].load = p[Raw].load.replace(b'52.205.63.231', generate_fake_ip('52.205.63.231').encode())
        p[Raw].load = p[Raw].load.replace(b'216.221.154.123', generate_fake_ip('216.221.154.123').encode())
        p[Raw].load = p[Raw].load.replace(b'216.221.154.122', generate_fake_ip('216.221.154.122').encode())
        p[Raw].load = p[Raw].load.replace(b'216.221.154.121', generate_fake_ip('216.221.154.121').encode())
        pass
    wrpcap(pcapfile.replace(".pcap", ".modified.pcap"), packets)
    
    
def modify_log(logfile):
    with open(logfile, 'r') as f:
        old = f.read()
        for ip in ip_map:
            old = old.replace(ip, ip_map[ip])
        with open(logfile.replace(".log", ".modified.log"), 'a') as lf:
            lf.write(old)
uuids = [
    "10b80cf1-5f41-45c0-85fb-b7cc9c6c89e1",
    "24eee4d2-87b4-4ff7-b0fc-ac6c44c61bca",
    "93622825-80b6-4ace-ae16-e7ef69a70020"
]
for f in uuids:
    modify_pcap("./ms-%s.pcap" % f)
    modify_log("./%s.log" % f)
print(ip_map)