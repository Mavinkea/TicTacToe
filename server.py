import socket
import sys
from thread import *
from threading import RLock
from player import Player
from tttgame import TTTGame

try:
	socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error:
	print('Could not create socket')

try:
    socket.bind(('', 6869))
except socket.error:
    print 'Failed'
    sys.exit()

socket.listen(2)
print 'Listening'

playerList=[]
gameList=[]
lock=RLock()

def connect(clientSock):

	while True:

		cmd=clientSock.recv(4096)

		#Login functionality
		req=cmd.split(" ")
		if req[0]=='login' and req[1]:
			username=req[1]
			found = False
			#Check if username exists already
			for p in playerList:
				if p.username==username:
					currPlayer=p
					found=True
					print currPlayer.username+" logged in"

			#Add a new player
			if not found:
				lock.acquire()
				currPlayer = Player(username,clientSock,"available")
				playerList.append(currPlayer)
				print currPlayer.username+ " created an account and logged in"
				lock.release()

			clientSock.send("Welcome: "+currPlayer.username)

		#Help functionality
		elif cmd=='help':
			clientSock.send("The different commands are: "
				+"\nlogin-create an account or log into an existing one"
				+"\nmove n-move to position n, where n is between 1 and 9"
				+"\nexit-leave the server")

		elif cmd=='place':
			game=TTTGame(1,2,3)
			print game.drawBoard()

		#Exit functionality	
		elif cmd=='exit':
			print 'Client disconnected'
			clientSock.send("DISCONN")
			clientSock.close()
			break

		else: 
			clientSock.send("400 ER")

while True:
	clientSock, addr=socket.accept()
	print 'Connected to a client'

	start_new_thread(connect, (clientSock,))

socket.close()


