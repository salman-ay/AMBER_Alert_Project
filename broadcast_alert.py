from socket import *
import time

# Set the IP address and port number of the broadcast server
ip_address = '192.168.1.255'
port_number = 5000

# Create socket that can broadcast
s = socket(AF_INET, SOCK_DGRAM)
s.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

# Bind the socket to the broadcast address and port number
s.bind(('', port_number))

# Get user input for the message
vehicle_color = input("Enter vehicle color: ")
vehicle_type = input("Enter vehicle type: ")
license_plate = input("Enter license plate number: ")
message = f"AMBER ALERT: Child abduction in progress. Suspect vehicle is a {vehicle_color} {vehicle_type}. License plate number {license_plate}."

# Send the AMBER alert message to all devices on the network
s.sendto(bytes(message, "utf-8"), (ip_address, port_number))

s.close()
