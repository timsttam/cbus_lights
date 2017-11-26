#!/usr/bin/env python

from scapy.all import *
from time import time, sleep
import socket

conf.iface = "mon0"


def handle_pkt(pkt):
    if Dot11 in pkt and pkt[Dot11].type == 0 and pkt[Dot11].subtype == 4:
        print "Handling packet type (0): %s subtype (4): %s" % (pkt[Dot11].type, pkt[Dot11].subtype)
        print "Found device %s" %pkt.addr2


while True:
    try:
        print "About to sniff"
        sniff(prn=handle_pkt,count=500)
	print "About to sleep"
        sleep(1)
    except KeyboardInterrupt:
        raise
    except:
        pass
