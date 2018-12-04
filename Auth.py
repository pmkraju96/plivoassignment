import pymysql

class Auth:
	def __init__(self, key):
		self.key = key
		self.db = pymysql.connect(host = '127.0.0.1',user='root',passwd='thanks123',db='plivo_assignment' )
		self.cursor = db.cursor()
		self.user = ""

	def authorize(self):
		val = self.cursor.execute("Select * from authtable where key = %s",(self.key))
		values = cursor.fetchall()
		if(len(values) > 1):
			self.user = values[0] 
			return True
		else:
			return False