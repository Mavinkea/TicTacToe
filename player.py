class Player:

	def __init__(self, username, conn):
		self.username=username
		self.conn=conn
		self.state="loggedin"

	def send(self, msg):
		self.conn.send(msg)

	def setAvailable(self):
		self.state="available"

	def setBusy(self):
		self.state="busy"

	def setLoggedIn(self):
		self.state="loggedin"



