import socket
import sys



sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server_address = ('192.168.159.128',5080)
print >>sys.stderr, 'starting up on %s port %s' % server_address
sock.bind(server_address)
# Listen for incoming connections
sock.listen(1)
version ='0.1.1'

while True:
    # Wait for a connection
    print >>sys.stderr, 'waiting for a connection'
    connection, client_address = sock.accept()
    try:
        print >>sys.stderr, 'connection from', client_address

        # Receive the data in small chunks and retransmit it
        while True:
            data = connection.recv(20)
            #connection.sendall(version)
            print >>sys.stderr, 'received "%s"' % data
            if data == 'request version':
                connection.sendall(version)
                update_req = connection.recv(30)
                print >>sys.stderr, 'Client Update request "%s"' % update_req
                if update_req == 'Is there an update?':
                    client_version = 'What is your version?'
                    connection.sendall(client_version) # To ask client version 
                    client_ver_ans = connection.recv(30)
                    print >>sys.stderr, 'Client version "%s"' % client_ver_ans
                    if (client_ver_ans < '1.1.2'):  # If less than 1.1.2 version No update available
                        server_res = 'No update available'
                        connection.sendall(server_res)
                    else:
                        service_res = 'Update available'
                        connection.sendall(service_res)
                        res = connection.recv(30)
                        print >>sys.stderr, 'client req "%s"' % res
                        download_url ='https://pypi.python.org/packages/source/F/Flask/Flask-0.10.1.tar.gz'
                        connection.sendall(download_url)

            else:
                print >>sys.stderr, 'no more data from', client_address
                break
            
    finally:
        # Clean up the connection
        connection.close()
