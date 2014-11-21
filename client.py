import socket
import sys
import urllib
import tarfile
import subprocess


# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('192.168.159.128', 5080)
print >>sys.stderr, 'connecting to %s port %s' % server_address
sock.connect(server_address)

try:
    
    # Send data
    message = 'request version'
    print >>sys.stderr, 'sending "%s"' % message
    sock.sendall(message)
    
    #while amount_received < amount_expected:
    while True:
        data = sock.recv(16)
        if data:
            print >>sys.stderr, ' Server version "%s"' % data
            update_request = 'Is there an update?' # Client Update request
            sock.sendall(update_request)
            server_quest = sock.recv(40)
            print >>sys.stderr, 'server question "%s"' % server_quest
            if server_quest == 'What is your version?':
               #version = '0.1.0'   # version 0.1.0  To check no update available use case
               version = '1.2.4'                    # pass different version number to get update from server '1.2.4' 
               sock.sendall(version)
               serv_resp = sock.recv(100)
               print >>sys.stderr, 'Server Update Response "%s"' % serv_resp
               if (serv_resp ==  'Update available'):
                   msg = 'Send Download url'
                   sock.sendall(msg)
                   download_url = sock.recv(600)
                   update_soft = urllib.URLopener()
                   update_soft.retrieve(download_url, "Flask-0.10.1.tar.gz")
                   file = tarfile.open('Flask-0.10.1.tar.gz')
                   file.extractall()
                   file.close()
                   dir_name = 'Flask-0.10.1'
                   subprocess.call(['pip', 'install', dir_name, 'processing'])
                   
            else:
                print >>sys.stderr, 'no more data from', server_address
                break
finally:
    print >>sys.stderr, 'closing socket'
    sock.close()

