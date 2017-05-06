import socket
import sys
import Queue
from thread import *
from threading import RLock
from player import Player
from tttgame import TTTGame
import time

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

players=[]
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
			for p in players:
				if p.username==username:
					currPlayer=p
					found=True
					print currPlayer.username+" logged in"

			#Add a new player
			if not found:
				lock.acquire()
				currPlayer = Player(username,clientSock)
				players.append(currPlayer)
				print currPlayer.username+ " created an account and logged in"
				lock.release()

			clientSock.send("Welcome: "+currPlayer.username)

		elif req[0]=='play':
			#Make player wait to find an opponent if none is available
			currPlayer.setAvailable()
			opponent=None
			while opponent is None:
				for opp in players:
					if opp.username!=currPlayer.username and opp.state=="available":
						opponent=opp

				#Use sleep function to wait until opponent is found
				if opponent is None:
					time.sleep(1)
				#Send message to current player and opponent that they are connected with eachother
				else:
					currPlayer.conn.send("WAIT Starting game with: "+opponent.username)
					opponent.conn.send("WAIT tarting game with: "+currPlayer.username)

		#Help functionality
		elif cmd=='help':
			clientSock.send("Commands: "
				+"\nlogin-create an account or log into an existing one"
				+"\nplace n-move to position n, where n is between 1 and 9"
				+"\nexit-leave the server")

		elif cmd=='place':
			game=TTTGame(1,2,3)
			clientSock.send(game.drawBoard())

		#Exit functionality	
		elif cmd=='exit':
			print'Client disconnected'
			clientSock.send("DISCONN")
			clientSock.close()
			break

		else: 
			clientSock.send("400 ERR")

while True:
	clientSock, addr=socket.accept()
	print 'Connected to a client'

	start_new_thread(connect, (clientSock,))

socket.close()


