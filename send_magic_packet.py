#!/usr/bin/env python

import logging
# Pour enlever les warnings inutiles de scapy
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import *
import netifaces
import sys

IFACE = 'eth1'

vlanList = {}
localmac = netifaces.ifaddresses(IFACE)[netifaces.AF_LINK][0]['addr']

def sendMagicPacket(mac, vlans, interface=IFACE):
    for i in vlans:
        wolpkt = Ether(dst='ff:ff:ff:ff:ff:ff') /Dot1Q(vlan=i) /IP(dst='255.255.255.255') /UDP(dport=7) /Raw('\xff'*6 + mac*16)
        sendp(wolpkt, iface=interface, verbose=False)


if __name__ == "__main__":
    mac = sys.argv[1].replace(":", "").replace("-", "").decode("hex")
    vlan = int(sys.argv[2])
    
    print "Magic packet pour %s sur le vlan %i"%(sys.argv[1], vlan)    
    sendMagicPacket(mac, [vlan])