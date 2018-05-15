#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Program Name: client.py
# anthonywww
# 05/13/2018 (MM/DD/YYYY)
# Python Version 3.4
# Description: A very rudimentary client emulator for testing the Project Delta Server protocol https://github.com/anthonywww/project-delta-server

# Optional import for versions of python <= 2
from __future__ import print_function

# Imports
import os
import sys
import time
import random
import socket
import platform

# Settings
HOST = '127.0.0.1'
PORT = 11234
BUFSIZE = 4096
STRC = "\u00A7"
DELIMITER = "|"
NAME = "PyDeltaClient"
VERSION = "0.1.0"

# Ensure the required cli-parameters are met
if len(sys.argv) != 3:
	print("Usage: %s <x> <y>" %(sys.argv[0]))
	sys.exit(1)

# Client attributes
CLIENT_ATTRIBUTES = {
	'name': NAME,
	'version': VERSION,
	'x': sys.argv[1],
	'y': sys.argv[2],
	'width': "800",
	'height': "600",
	'os': "%s %s" %(platform.system(), platform.release()),
	'cpu': "Test(r) %s Python" %(STRC),
	'gpu':  "None",
	'memory': "1024"
}

# Variables
PACKET_HEADER = {
	'DISCONNECT': 0x00,
	'HANDSHAKE': 0x01,
	'HANDSHAKE_ACK': 0x02,
	'SYNC': 0x03,
	'SYNC_ACK': 0x04,
	'MESSAGE_DATA': 0x05,
	'PLAY_TEXT': 0x06,
	'PLAY_TEXT_DELETE': 0x07,
	'PLAY_TEXT_ACK': 0x08,
	'PLAY_TEXT_DELETE_ACK': 0x09,
	'PLAY_AUDIO': 0x0A,
	'PLAY_AUDIO_ACK': 0x0B,
	'PLAY_AUDIO_FIN': 0x0C,
}

current_time_in_millis = lambda: int(round(time.time() * 1000))

print("%s v%s - Client # [%s,%s]" %(NAME,VERSION,CLIENT_ATTRIBUTES['x'],CLIENT_ATTRIBUTES['y']))
handshake_stage = 0
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect
try:
	print("[Client] Dialing server %s:%s ..." %(HOST, PORT))
	sock.connect((HOST, PORT))
except ConnectionRefusedError:
	print("[Client] Connection refused! (is the server running?)")
	sys.exit(1)

print("[Client] Connected! [%s, %s]" %(CLIENT_ATTRIBUTES['x'], CLIENT_ATTRIBUTES['y']))

# Initiate connection handshake (greetings, my name is client, what's your name?)
client_hello = bytearray()
client_hello.append(PACKET_HEADER['HANDSHAKE'])

i = 0
for key,value in CLIENT_ATTRIBUTES.items():
	if i < len(CLIENT_ATTRIBUTES) and i != 0:
		client_hello.extend(map(ord, DELIMITER))
	
	client_hello.extend(map(ord, value))
	i = i + 1
	
sock.sendall(client_hello)
print("Sent <- %s" %(client_hello))

# Loop
while True:
	try:
		# Read 4096 bytes from socket
		raw_data = sock.recv(BUFSIZE)
		
		# Check if the socket was closed
		if not raw_data:
			print("[Client] Server closed connection")
			sock.close()
			break
		
		data = bytearray(raw_data)
		header = data[0]
		payload = data[1:]
		header_name = "UNKNOWN"
		
		# Set the header_name via a reverse-lookup of the PACKET_HEADER dict
		for key,value in PACKET_HEADER.items():
			if header == value:
				header_name = key
		
		# Print info
		print("Recv -> [%s] Payload: %s" %(header_name,payload))
		
		# Got a disconnect request, close the socket
		if header == PACKET_HEADER['DISCONNECT']:
			print("[Client] Got disconnect packet, hanging-up ...")
			break
		
		# Got a handshake acknowledgement
		if header == PACKET_HEADER['HANDSHAKE_ACK']:
			print("[Client] Woo! We got a handshake acknowledgement! '%s'" %(payload.decode("utf-8")))
		
		# Got a heartbeat, acknowledge the request
		if header == PACKET_HEADER['SYNC']:
			#print (int.from_bytes(payload, byteorder='big'))
			hb = bytearray()
			hb.append(PACKET_HEADER['SYNC_ACK'])
			hb.extend(map(ord, "%d" %(current_time_in_millis())))
			sock.sendall(hb)
			print("Sent <- %s" %(hb))
		
	except ConnectionResetError:
		print("")
		print("[Client] Host closed connection without the DISCONNECT header")
		break
	except KeyboardInterrupt:
		print("")
		print("Caught system interrupt, ending conversation ...")
		dc = bytearray()
		dc.append(PACKET_HEADER['DISCONNECT'])
		sock.sendall(dc)
		print("Sent -> %s" %(dc))
		break

sock.close()
print("[Client] Hung-up.")
sys.exit(0)



