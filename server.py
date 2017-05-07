import socket
import sys
import Queue
from thread import *
from threading import RLock
from player import Player
from tttgame import TTTGame
import time
import uuid

#Create server socket object
try:
	socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error:
	print('Could not create socket')

#Bind to port 6869
try:
    socket.bind(('', 6869))
except socket.error:
    print ('Failed')
    sys.exit()

socket.listen(5)
print 'Listening'

#Keeps track of players currently in the server
players=[]
#Keeps track of games currently underway. Stores UUID objects.
gameList=[]
lock=RLock()

def connect(clientSock):
	"""Run for each client that connects to the server
	Handles messages sent from the client and sends corresponding responses"""

	#Opening message to client. Also breaks initial client WAIT loop, allowing the client to send input
	clientSock.send("Welcome to Tic Tac Toe")

	#Main connection loop. Handles all messages from client
	while True:
		#Command sent by client
		cmd=clientSock.recv(4096)
		#Login functionality
		req=cmd.split(" ")
		#Checks that user is asking to login, and also has specified a username
		if req[0]=='login' and req[1]:
			username=req[1]
			found = False
			#Check if username exists already
			for p in players:
				#If it does, then the user logged back in. No need to create a new user
				if p.username==username:
					currPlayer=p
					found=True
					print currPlayer.username+" logged in"

			#Add a new player if no user with specified username exists
			if not found:
				lock.acquire()
				#Create player object with this thread's client socket and the user specified username
				currPlayer = Player(username,clientSock)
				players.append(currPlayer)
				print currPlayer.username+ " created an account and logged in"
				lock.release()

			clientSock.send("Welcome: "+currPlayer.username)

		#Play functionality
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
				#Once an opponent is found, generate a gameID, add it to the list of current games,
				#and create a game with the found opponent and the current player
				else:
					lock.acquire()
					id=uuid.uuid4()
					game=TTTGame(opponent, currPlayer, id)
					print "New Game with id: "+str(id)
					gameList.append(game.gameID)
					currPlayer.setBusy()
					opponent.setBusy()
					lock.release()

					#See below for startGame documentation
					startGame(game)

					#Once the game is finished, removethe game from the list of current games
					#and set the two player's states back to loggedin
					lock.acquire()
					gameList.remove(id)
					currPlayer.setLoggedIn()
					opponent.setLoggedIn()
					lock.release()

		#List all available games
		elif cmd=="games":
			if len(gameList)>0:
				listOfGames=""
				for g in gameList:
					listOfGames+=str(g+"\n")
				clientSock.send(listOfGames)
			else:
				clientSock.send("No games currently")

		#List all players logged 
		elif cmd=="who":
			if len(players)>0:
				listOfPlayers=""
				for p in players:
					listOfPlayers+=str(p.username+"\n")
				clientSock.send(listOfPlayers)
			else:
				clientSock.send("No players currently")

		#Help functionality
		elif cmd=='help':
			clientSock.send("Commands: "
				+"\nlogin username-Enter login followed by a username of your choice."
				+"\nplay-Finds and starts a game, or waits until a game is found. Must be logged in to play"
				+"\nplace n-Move to position n, where n is between 0 and 8. Must be logged in and in a game to use this command."
				+"\ngames-Show all games currently going on."
				+"\nwho- Show all players currently logged in or playing a game"
				+"\nexit-Leave the server.")

		#Exit functionality	
		elif cmd=='exit':
			print'Client disconnected'
			clientSock.send("DISC")
			clientSock.close()
			break

		else: 
			clientSock.send("400 ERR")

def startGame(game):
	"""Contains the main game loop
	Takes a TTTGame object as an argument"""

	gameover=False

	#Main game loop
	while not gameover:
		game.turn.send("Your turn")
		game.waiting.send("WAIT Other players turn")
		move=game.turn.conn.recv(4096)
		if checkMove(game,move):
			response=game.makeMove(move.split(" ")[1])

			#Case: Move is valid but not game ending
			#Give both players an update of the game board and switch turns. Continue with game loop.
			if response=="301 NPT":
				game.turn.send("WAIT"+game.drawBoard())
				game.waiting.send("WAIT"+game.drawBoard())
				game.changeTurn()

			#Case: Game finished and no winner.
			#Notify players that it is a draw and exit game loop
			elif response=="300 FIN":
				gameover=True
				game.turn.send("No winner")
				game.waiting.send("No winner")

			#Case: Game finished and winner
			#Notify players who won and exit game loop
			elif response=="300 WIN":
				gameover=True
				game.turn.send("Game over. You won!")
				game.waiting.send("Game over. "+game.turn.username+" won!")
				print "Game over"
		else:
			continue
	return

def checkMove(game, move):
	"""Takes a player move as argument
	and ensures that the move is valid."""
	try:
		statement, pos=move.split(" ")
		pos=int(pos)
	except ValueError:
		return False

	#First check that the user has properly requested to place
	if statement !="place":
		return False

	#Then check that the user's choice is a valid board position	
	elif pos<0 or pos>8 or game.board[pos]=='X' or game.board[pos]=='O':
		return False

	else:
		return True

#Main loop
while True:
	clientSock, addr=socket.accept()
	print 'Connected to a client'

	start_new_thread(connect, (clientSock,))

socket.close()


