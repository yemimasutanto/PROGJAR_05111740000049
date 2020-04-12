import sys
import socket
import os

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Bind the socket to the port
server_address = ('127.0.0.1', 10000)
print(f"starting up on {server_address}")
sock.bind(server_address)
# Listen for incoming connections
sock.listen(1)
while True:
    # Wait for a connection
    print("Waiting for a Connection")
    connection, client_address = sock.accept()
    print(f"connection from {client_address}")
    # Receive the data in small chunks and retransmit it
    filename = ''
    while True:
        data = connection.recv(1024).decode('utf-8')
        if not data:
            break
        print(f"received {data}")
        filename += data
    if os.path.isfile(filename):
        print("Sending: " + filename)
        myfile = open(filename, "rb")
        connection.send(myfile.read())
    else:
        print("File not Found!")
        connection.send(myfile.read())

    # Clean up the connection
    connection.close()
