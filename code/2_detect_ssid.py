#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#################################################################
# File name:    2_detect_ssid.py
# Author:       Frueh Loïc & Muaremi Dejvid
# Date:         15.03.2019
# Lecture:      SWI
# Purpose:      This script sniff all probe requests and
#               make a list of all SSID per MAC addresses found
#################################################################
from scapy.all import sniff
from threading import *
import time
import argparse
import re
import json
import requests
import os

# Argument parser
parser = argparse.ArgumentParser('SSID detector')
parser.add_argument('--interface', '-i', type=str, default='wlan0mon', help='name of your wi-fi interface')
parser.add_argument('--api', '-a', type=str, default='http://macvendors.co/api/%s', help='web api interface')
args = parser.parse_args()

# utiliser un dictionnaire pour stocker le adresse mac et la liste des SSID (par address MAC)
macs_SSIDs_list = {}

lock = Lock()
# <--- Function that update our dictionary of SSID (in function of MAC address) --->
def update_macs_ssid_list(packet):
    lock.acquire()
    # The packet is a wifi packet and a probe request
    if packet.type == 0 and packet.subtype == 4:
        MAC_address = packet.addr2.upper()
        SSID = packet.info.decode('utf-8')
        # The MAC found is not yet in the dictionnary
        if MAC_address not in macs_SSIDs_list:
            macs_SSIDs_list[MAC_address] = []
        # The SSID found is not yet in the SSID list of this MAC adresse
        if SSID not in macs_SSIDs_list.get(MAC_address):
            macs_SSIDs_list.get(MAC_address).append(SSID)
    lock.release()


# <--- Function that display the result every 5 sec --->
def display_results():
    while True:
        lock.acquire()
        os.system('clear')
        print('------- Devices and SSIDs found -------------------------------------')
        for mac in macs_SSIDs_list.keys():
            try:
                req = requests.get(args.api % mac)
                constructor = req.json()['result']['company']
            except:
                constructor = 'UNKNOW'
            print("%s (%s) - %s" % (mac, constructor, ', '.join(list(filter(None,macs_SSIDs_list.get(mac))))))
        lock.release()
        time.sleep(5)

def start_sniff():
    sniff(iface=args.interface, prn=update_macs_ssid_list)


try:
    # Created the threads to sniff and display the SSIDs
    display = Timer(1.0, display_results)
    sniffer = Timer(0.0, start_sniff)  

    # Start the threads as daemons
    sniff.daemon = True
    sniffer.start()
    display.daemon = True
    display.start()

    while(True):
        sniffer.join(1)
        display.join(1)
except KeyboardInterrupt:
    exit(1)