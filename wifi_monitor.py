#!/usr/bin/env python

from scapy.all import *
# from time import localtime, time, sleep, strftime
import time
import socket

conf.iface = "mon0"

server_ip = '172.17.1.222'
server_port = 11001

# Time since last seen do we declare the device as having returned home
lasthome = 300
# Create a dictionary for devices - will end up being populated with MAC:lastseen_epoch
devices = {}

def handle_pkt(pkt):
    if Dot11 in pkt and pkt[Dot11].type == 0 and pkt[Dot11].subtype == 4:
        newdev = check_device(pkt.addr2)
        if newdev is not None:
            print '	Notifying server of %s' % newdev
            notify(newdev)
	devices[pkt.addr2] = int(time.time())

def check_device(dev):
    rightnow = int(time.time())
    datetime_string = time.strftime("%H:%M:%S %d/%m/%Y",time.localtime(rightnow))
    print "Checking %s at %s (%s)" % (dev, datetime_string, rightnow)
    if dev in devices:
        datetime_string = time.strftime("%H:%M:%S %d/%m/%Y",time.localtime(devices.get(dev)))
        print "		Last seen %s (%s)" % (datetime_string, devices.get(dev))
        # if rightnow epoch minus last device seen epoch is greater than last home
        diff = rightnow-devices.get(dev)
        if diff > lasthome:
            #print "Welcome home %s" %dev
            return dev
        #else:
        #    print "%s last seen %s ago" % (dev, diff)
    else:
        print "		New device %s" % (dev)
        return dev

def notify(newdev):
    # Connect to server
    s = socket.socket()
    try:
        s.connect((server_ip, server_port))
        # send newdev MAC address
        s.send(newdev)
        confirmdev = s.recv(20)
        # if not ok resend
        if newdev == confirmdev:
            s.send('OK')
        # disconnect
        s.close
    except:
        pass
    


while True:
    try:
        sniff(iface="mon0",prn=handle_pkt,count=500)
        time.sleep(1)
    except KeyboardInterrupt:
        raise
    except:
        pass
