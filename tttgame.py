class TTTGame:

	def __init__(self, player1, player2, gameID):
		self.player1=player1
		self.player2=player2
		self.gameID=gameID
		self.turn=player1
		self.waiting=player2
		self.board=[' 0 ',' 1 ',' 2 ',' 3 ',' 4 ',' 5 ',' 6 ',' 7 ',' 8 ']

	def drawBoard(self):
		return self.board[0]+" | "+self.board[1]+" | "+self.board[2]+"\n"+self.board[3]+" | "+self.board[4]+" | "+self.board[5]+"\n"+self.board[6]+" | "+self.board[7]+" | "+self.board[8]

	def changeTurn(self):
		if self.turn==self.player1:
			self.turn=self.player2
			self.waiting=self.player1
		else:
			self.turn=self.player1
			self.waiting=player2

