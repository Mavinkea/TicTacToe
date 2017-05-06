import socket
import sys

try:
	socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error:
	print("Could not create socket")

script,host = sys.argv

socket.connect((host, 6869))
response="WAIT"

while True:

	while "WAIT" in response:
		response=socket.recv(4096)
		print response

	userInput=raw_input("ttt->")
	if(userInput==''):
		continue

	socket.send(userInput)
	response=socket.recv(4096)

	if response=="400 ERR":
		print "Invalid command"

	else:
		print response

		if response=="DISCONN":
			sys.exit()



socket.close()
