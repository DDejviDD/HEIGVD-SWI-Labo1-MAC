#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#################################################################
# File name:    1_detect_mac.py
# Author:       Frueh Loïc & Muaremi Dejvid
# Date:         15.03.2019
# Lecture:      SWI
# Purpose:      This script sniff all probe requests and
#               make a list of all MAC addresses given
#               as argument found
#################################################################
from scapy.all import sniff
import argparse, re

# Argument parser
parser = argparse.ArgumentParser('MAC addresses detector')
parser.add_argument('--interface', '-i', type=str, default='wlan0mon', help='name of your wi-fi interface')
parser.add_argument('MAC_addresses', nargs='*')
args = parser.parse_args()

# List of MAC already detected and found
mac_found = []


# <--- Function that display the MAC address of a packet if it has been given as argument --->
def display_if_mac_address_found(packet):
    # The packet is a wifi packet and a probe request
    if packet.type == 0 and packet.subtype == 4: 
        if packet.addr2.upper() in mac_addresses:
                print('Device with MAC : %s has been found!' %(packet.addr2.upper()))


# Check if there is at least one mac address to search for
if len(args.MAC_addresses) < 1:
    print('You must provide at least one MAC address as an argument !!!')
    exit(1)

# Prepare a map for all the MAC given by the user
mac_addresses = list(map(str.upper, args.MAC_addresses))

# Check if the MAC are valid with a super regular expression
mac_regex = re.compile('^([0-9A-F]{2}[:-]){5}([0-9A-F]{2})$')

for m in mac_addresses:
    if not bool(mac_regex.fullmatch(m)):
        print('You have at least one wrong MAC address format in your entry.')
        exit(1)

print ('Number of MAC addresses   :', len(mac_addresses))
print ('List of the MAC addresses :', str(mac_addresses))

# Start the scapy sniffer and call our custom scanner
sniff(iface=args.interface, prn=display_if_mac_address_found)
