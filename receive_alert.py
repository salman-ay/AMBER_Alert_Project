from socket import *
import datetime

# Set the IP address and port number of the broadcast server
ip_address = '192.168.1.255'
port_number = 5000

# Create a UDP socket
s = socket(AF_INET, SOCK_DGRAM)

# Bind the socket to the broadcast address and port number
s.bind((ip_address, port_number))

while True:
	data, addr = s.recvfrom(1024)
	message = data.decode('utf-8')
	print(message)
	current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	print("Date and Time: {}".format(current_time))
	if message.startswith("AMBER ALERT:"):
		info = message.split(".")
		color_type = info[1].split(" ")
		color = color_type[5]
		vehicle_type = color_type[6]
		license_plate = info[2].split(" ")[-1]
#		print("Received AMBER Alert:")
#		print("Vehicle color: {}".format(color))
#		print("Vehicle type: {}".format(vehicle_type))
#		print("License plate: {}".format(license_plate))
