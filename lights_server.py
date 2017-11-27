#!/usr/local/python
from __future__ import print_function

# Version 0.01

## Change Log

# 20171127 0.01
#  Added client connection handling (rough code)
#  Process passed devices; turn on lights via pydbus call

## To-Do:
##
## Read devices from local file
## Check for sunset, turn lights on; check for sunrise, turn lights off
## Store devices and times received from clients

matt_s7 = ''

import sys
import socket
from pydbus import SystemBus

LISTEN_HOST=''
LISTEN_PORT=11001

SUNSET_LIGHTS = {11} # 11 Front porch
HOME_LIGHTS = {11,12,15} # 11 Front porch, 15 Hallway, 12 Kitchen Bench
ALREADY_HOME_LIGHTS = {12} # 12 Kitchen Bench
SUNSET_LIGHTS_ON = '/tmp/sunset_lights_on'

def turn_on(LIGHTS):
   print ("Known-device confirmed, turning on lights %s" % LIGHTS)
# mdbus2 -s au.id.micolous.cbus.CBusService / au.id.micolous.cbus.CBusInterface.lighting_group_on "(${1})"
   bus = SystemBus()
   cbus = bus.get('au.id.micolous.cbus.CBusService', '/')
   cbus_api = cbus['au.id.micolous.cbus.CBusInterface']
   for light in LIGHTS:
      lightb = bytes(bytearray([light]))
      #print type(lightb)
      #print "Light %s in Bytes is %s" % (light,str(lightb))
      cbus_api.lighting_group_on(lightb)

def handle_device(DEVICE):
   print ("Handling device %s" % DEVICE)
   if DEVICE == matt_s7:
      turn_on(HOME_LIGHTS)
   else:
      print ("Unknown device")

# Main Server for client connections
def server():
   try:
      s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   except socket.error:
      print ("Failed to create socket")
      sys.exit()
   print ("Listening for connections on port %s" % LISTEN_PORT)
   s.bind((LISTEN_HOST,LISTEN_PORT))
   
   # listen for connections
   s.listen(5)

   while True:
      c, addr = s.accept()                      # Process connection
      # device received - receive 20 bytes
      THIS_DEV = c.recv(20)                     # Receive 20 bytes following connection
      print ("Received device %s" % THIS_DEV)
      c.send(THIS_DEV)                          # Send device back; expect 'OK'
      print ("Sending confirmation...", end='')
      if c.recv(2) == 'OK':
         print ("OK, confirmed device received %s" % THIS_DEV)
         handle_device(THIS_DEV)
      else:
         print ("NOT OK, closing connection")
      c.close()
   

if __name__ == '__main__':
    server()
