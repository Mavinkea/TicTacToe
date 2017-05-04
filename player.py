class Player:

	def __init__(self, username, conn, state):
		self.username=username
		self.conn=conn
		self.state=state

	def changeState(self, state):
		self.state=state

	def send(self, msg):
		self.conn.send(msg)



