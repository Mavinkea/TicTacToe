class Player:

	"""Player object has three states (loggedin, available, and busy)
	loggedin indicates that the user has logged in isnt searching for a game yet
	available indicates that the user is searching for a game
	busy indicates that the user is in game"""

	def __init__(self, username, conn):
		"""Constructor for player object"""
		self.username=username
		self.conn=conn
		self.state="loggedin"

	def send(self, msg):
		"""Send a message through player's connection"""
		self.conn.send(msg)

	def setAvailable(self):
		"""Make available"""
		self.state="available"

	def setBusy(self):
		"""Make busy"""
		self.state="busy"

	def setLoggedIn(self):
		"""Make loggedin"""
		self.state="loggedin"



