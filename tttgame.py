class TTTGame:

	def __init__(self, player1, player2, gameID):
		"""Constructor for a Tic Tac Toe game
		Represens one game between two players"""
		self.player1=player1
		self.player2=player2
		self.gameID=gameID
		self.turn=player1
		self.waiting=player2
		self.board=['0','1','2','3','4','5','6','7','8']
		self.WIN_COMBINATIONS = [(0, 1, 2),(3, 4, 5),(6, 7, 8),(0, 3, 6),(1, 4, 7),(2, 5, 8),(0, 4, 8),(2, 4, 6),]

	def drawBoard(self):
		"""Returns a string formatted to represent the Tic Tac Toe board"""
		return "\n"+self.board[0]+" | "+self.board[1]+" | "+self.board[2]+"\n"+self.board[3]+" | "+self.board[4]+" | "+self.board[5]+"\n"+self.board[6]+" | "+self.board[7]+" | "+self.board[8]

	def changeTurn(self):
		"""Automatically switches turn. Used in main game loop to go back and forth between players"""
		if self.turn==self.player2:
			self.turn=self.player1
			self.waiting=self.player2
		else:
			self.turn=self.player2
			self.waiting=self.player1

	def makeMove(self, move):
		"""Adds either an X or O to the game board
		and checks whether game is still in progress or not.
		Takes one argument, a number between 0 and 8"""
		move=int(move)
		if self.turn==self.player1:
			self.board[move]='X'
		else:
			self.board[move]='O'

		done=True
		#Check if there are still moves to be made
		for i in self.board:
			if i!='X' or i!='O':
				done=False

		#Check for winning combinations
		#If winning combination is found, the game is over
		for a,b,c in self.WIN_COMBINATIONS:
			if self.board[a]==self.board[b]==self.board[c]:
				done=True

		#Endgame
		#300 FIN- Game Finished
		if done:
			return "300 FIN"
		#If not endgame, indicate to server that the game loop must continue running
		#301 NPT- Next Player Turn
		else:
			return "301 NPT"

			
