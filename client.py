import socket
import sys

#Create socket object
try:
	socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error:
	print("Could not create socket")

#Use host that user input
script,host = sys.argv

#Connect to a remote socket at specified host address
socket.connect((host, 6869))
#Initial response
response="WAIT"

"""Client loop. Always either waiting for further instructions and not taking user input
or taking user input and returning server response"""
while True:

	while "WAIT" in response:
		response=socket.recv(4096)
		print response

	#Take user input from command line interface
	userInput=raw_input("ttt->")
	if(userInput==''):
		continue

	#Send user input to server, and collect response
	socket.send(userInput)
	response=socket.recv(4096)

	#Error handling
	if response=="400 ERR":
		print "Invalid command"

	#If response is valid, print it
	else:
		print response

		#Exit loop and quit program if user chooses to exit
		if response=="DISC":
			sys.exit()

socket.close()
