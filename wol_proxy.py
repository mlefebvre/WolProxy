#!/usr/bin/env python

import logging
# Pour enlever les warnings inutiles de scapy
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import *
import netifaces
from send_magic_packet import *
from vlan_finder import *

IFACE = 'eth1'

localmac = netifaces.ifaddresses(IFACE)[netifaces.AF_LINK][0]['addr']

def udp_monitor_callback(pkt):
      if pkt.haslayer(Raw):
          data = pkt.getlayer(Raw).load
          if len(data) == 102:
              if data.startswith(chr(0xff) * 6):
                  if pkt.src != localmac and pkt.src != '00:00:00:00:00:00':
                      mac = data[6:12]
                      macstr = mac.encode("hex")
                      macstr = "-".join([macstr[0:2], macstr[2:4], macstr[4:6], macstr[6:8], macstr[8:10], macstr[10:12]])
                      vlan = findVlan(macstr)               
                      print "Magic packet pour %s sur les vlans: %s"%(macstr, ":".join([str(v) for v in vlan]))
                      sendMagicPacket(mac, vlan, IFACE)         

        
sniff(prn=udp_monitor_callback, filter="udp", iface=IFACE)
