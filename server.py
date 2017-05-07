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
    print ('Failed')
    sys.exit()

socket.listen(2)
print 'Listening'

players=[]
gameList=[]
lock=RLock()

def connect(clientSock):

	clientSock.send("Welcome to Tic Tac Toe")

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

		elif req[0]=='play' and currPlayer:
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
					lock.acquire()
					game=TTTGame(opponent, currPlayer, 1)
					currPlayer.setBusy()
					opponent.setBusy()
					gameList.append(game.gameID)
					lock.release()
					startGame(game)

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

def startGame(game):

	gameover=False

	while not gameover:
		game.turn.send("Your turn")
		game.waiting.send("WAIT Other players turn")
		move=game.turn.conn.recv(4096)
		if checkMove(game,move):
			response=game.makeMove(move.split(" ")[1])

			if response=="301 NPT":
				game.turn.send("WAIT"+game.drawBoard())
				game.changeTurn()

			elif response=="300 FIN":
				gameover=True
				game.turn.send("Game over. You won!")
				game.waiting.send("Game over. "+game.turn.username+" won!")
				print "Game over"
		else:
			game.turn.send("Invalid move")

	return

def checkMove(game, move):
		statement, pos=move.split(" ")
		try:
			pos=int(pos)
		except ValueError:
			return False

		if statement !="place":
			return False
		elif pos<0 or pos>8 or game.board[pos]=='X' or game.board[pos]=='O':
			return False

		else:
			return True

while True:
	clientSock, addr=socket.accept()
	print 'Connected to a client'

	start_new_thread(connect, (clientSock,))

socket.close()


