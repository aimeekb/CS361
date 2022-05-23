# Microservice - Client side
# Author: Aimee Bogle
# This python program establishes a socket for communitcaion, as the client side. It will bind a host and port to create 
# the socket, and then send the request to the server side. The program will prompt the user for an address to geocode, 
# and it will transmit this address through the socket to the server. The server transmits the request and responds back 
# with the lat/lng coordinates. It will also print status messages on sending/receiving during processing. 
# NOTE: To successfully geocode, a full address is needed, to include zipcode. The address should look as follows:
# 12134 Washington st Los Angeles, CA 90201

import socket


def socket_client(add):
    """ Socket client-side, accepts address to transmit to server side """

    HOST = "127.0.0.1"
    PORT = 62545
    REQUEST = add

    # Creating the socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # Connecting to the host and port
        s.connect((HOST, PORT))

        # Printing the request
        print("Request: ", REQUEST)

        # Sending the request
        s.send(bytes(REQUEST, 'utf8'))

        # Retrieving the answer
        answer = s.recv(1024)

        # Printing the answer
        print("[RECV] - length: ", len(answer))
        print(answer)

        # Closing the socket
        s.close()

    return answer
    

if __name__ == '__main__':
    socket_client()
