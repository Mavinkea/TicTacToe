class Player:

	def __init__(self, username, conn):
		self.username=username
		self.conn=conn
		self.state="available"

	def changeState(self):
		if self.state=="available":
			self.state="busy"
		else:
			self.state="available"

	def send(self, msg):
		self.conn.send(msg)



