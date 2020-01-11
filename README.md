DESCRIPTION:
============
A simple client/server ping script written in python3, ping is sent over TCP or UDP. 

the user can set the protocol, socket timeout, the packet size, and the number of packets sent for each ping.

CONFIGURATION:
==============
each folder contains a config file.
## Configurable parameters:
HOST - server & client

TCP_PORT - server & client

UDP_PORT - server & client

BUFFER_SIZE - max bytes to receive from socket - server & client

DEF_TIMEOUT - set the default socket timeout - client

DEF_PACKET_NUM - set the default packet num each ping - client

DEF_PACKET_SIZE - set the packet size in bytes - client


EXECUTE:
========

To start the server run:
`python3 pingServer.py`

To run the client:
`python3 pingClient.py PROTOCOL [TIMEOUT] [PACKET_SIZE] [PACKET_NUM]`

Except for the Protocol (UDP or TCP) the rest of the arguments are optional

Examples:
 
 `python3 pingClient.py UDP` 
 
 `python3 pingClient.py TCP 4 64`