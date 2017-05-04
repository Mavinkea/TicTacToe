import socket
import sys

try:
	socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error:
	print("Could not create socket")

script,host,port = sys.argv
port=int(port)

socket.connect((host, port))
response="WAIT"

while True:

	while response != 'DISCONN':
		userInput=raw_input("ttt->")

		if(userInput==''):
			continue

		socket.send(userInput)
		response=socket.recv(4096)

		if response=="400 ER":
			print "Invalid command"

		if response=="DISCONN":
			sys.exit()

		print response


socket.close()
