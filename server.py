#import socket module
from socket import *
import sys # In order to terminate the program
from threading import Thread, Event
import time




server_Name=''
port_number=5448

serverSocket = socket(AF_INET, SOCK_STREAM)

# Prepare/Setup a sever socket
serverSocket.bind((server_Name, port_number))
serverSocket.listen(1)
print('listening...')
go=True
while go:
    #Establish the connection
    print('Ready to serve...')
    try:
        connectionSocket,addr = serverSocket.accept() #Fill in start #Fill in end

        # Receive message HTTP request from client
        message = connectionSocket.recv(1024).decode()
        # print(message)
        filename = message.split()[1]
        request = message.split()
        # print(filename)
        # print(request[2])
        f = open(filename)

        # Send the HTTP header line into socket
        outputdata = request[2]+' 200 OK\n'
        for lines in f:
            # print(lines)
            outputdata += lines # Add code to store contents of file
        print(outputdata)
        #Send the content of the requested file to the client
        connectionSocket.send(outputdata.encode())
        connectionSocket.send("\r\n".encode())
        f.close()
    except IOError:
        # Send response message for file not found
        # Close client socket
        connectionSocket.send((request[2]+'404 File not Found').encode())
        print('Cannont find file. Closing Socket...')
    except FileNotFoundError:
        connectionSocket.send((request[2]+'404 File not Found').encode())
        print(request[2]+'File not found. Closing Socket...')
    except:
        connectionSocket.send((request[2]+'400 Bad Request').encode())
        print('Unknown error. Closing Socket...')
    finally:
        serverSocket.close()
        go=False

connectionSocket.close()
sys.exit() #Terminate the program after sending the corresponding data

