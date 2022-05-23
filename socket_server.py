# Microservice for geocoding
# Author: Aimee Bogle
# This python program establishes a socket for communitcaion (server side). It will bind a host and port to create 
# the socket, and then listen for activty on the socket for a request. The client side collects and address to be converted 
# to lat/lng coordinates and transmits the data through the socket. When the data is receieved this program will send the 
# request to the Google Maps API to recieve the data and trasmit the coordinates back through socket. Once the data is sent 
# the socket connection will automatically close for security.  

import socket
import json
import urllib
import requests


def socket_server():
    """ Listens on socket for requests, transmits to Google API for conversion """

    HOST = "127.0.0.1"
    PORT = 62545
    base_url= "https://maps.googleapis.com/maps/api/geocode/json?"
    AUTH_KEY = '< API Key Here >'
    server_address = (HOST, PORT)

    # Creating the socket
    print('Server listening on: {} port: {}'.format(*server_address))

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # Binding the host and port
        s.bind((HOST, PORT))
        # Listening for the incoming connection
        s.listen(5)
        # Accepting the connection
        conn, addr = s.accept()


        with conn:
            print('Connected by', addr)
            
            # Retrieving the request
            request = b''
            request = conn.recv(1024)

            # Printing the request
            print("Received: ", request)
            parameters = {"address": request,
                "key": AUTH_KEY}
            
            # Use this line during troubleshooting to ensure correct URL is generated
            print(f"{base_url}{urllib.parse.urlencode(parameters)}")
            
            r = requests.get(f"{base_url}{urllib.parse.urlencode(parameters)}")
            data = json.loads(r.content)
            coord = data.get("results")[0].get("geometry").get("location")
            print(coord)
        
            # Sending the answer
            print()
            print("Sending>>>>>>>>")
            print(coord)
            coord_str = (str(coord))
            print(coord_str)
            conn.sendall(bytes(coord_str, encoding='utf8'))
            print("<<<<<<<<")

            # Closing the socket
            conn.close()


if __name__ == '__main__':
    socket_server()
