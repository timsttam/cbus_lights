#!/usr/local/python

# Version 0.01

## Change Log

# 20171127 0.01
# Added client connection handling (rough code)

## To-Do:
##
## Check for sunset, turn lights on; check for sunrise, turn lights off
## Store devices and times received from clients

import sys
import socket

LISTEN_HOST=''
LISTEN_PORT=11001

SUNSET_LIGHTS = '11' # 11 Front porch
HOME_LIGHTS = '11,12,15' # 11 Front porch, 15 Hallway, 12 Kitchen Bench
ALREADY_HOME_LIGHTS = '12' # 12 Kitchen Bench
SUNSET_LIGHTS_ON = '/tmp/sunset_lights_on'

def turn_on(LIGHTS):
# mdbus2 -s au.id.micolous.cbus.CBusService / au.id.micolous.cbus.CBusInterface.lighting_group_on "(${1})"
   

# Main Server for client connections
def server():
   try:
      s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   except socket.error:
      print "Failed to create socket"
      sys.exit()
   print "Listening for connections on port %s" % LISTEN_PORT
   s.bind((LISTEN_HOST,LISTEN_PORT))
   
   # listen for connections
   s.listen(5)

   while True:
      # process connection
      c, addr = s.accept()
      print "Received connection from ", addr
      # device received - receive 20 bytes
      THIS_DEV = c.recv(20)
      # send device back; receive 'OK'
      print "Received device ", THIS_DEV
      c.send(THIS_DEV)
      print "Sending confirmation..."
      if c.recv(2) == 'OK':
         # if OK, process device, else resume listen
         print "OK, confirmed device received ", THIS_DEV
      else:
         print "Did not receive OK, closing connection"
      c.close()
   

if __name__ == '__main__':
    server()
