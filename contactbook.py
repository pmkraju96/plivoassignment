from flask import Flask,request
import pymysql
import Auth

app = Flask(__name__)

db = pymysql.connect(host = '127.0.0.1',user='root',passwd='thanks123',db='plivo_assignment' )
cursor = db.cursor()
values = None


def authorize(key):
	val = cursor.execute("Select * from authtable where keyval = %s",(key))
	values1 = cursor.fetchall()
	print(len(values1))
	if(len(values1) >= 1): 
		return values1
	else:
		return False




#------------------------------------- Default function for api ---------------------------------------------------------#
@app.route("/")
def home():
	key = request.args.get("key",None)
	if(key):
		authvalue = authorize(key)
		if(authvalue):
			return ("Welcome to the Contact Book Api"+authvalue[0][0])
		else:
			return "invalid key access denied"
	else:
		return "please provide access key for api"
#---------------------------------- Function for adding the Contact -----------------------------------------------------#
@app.route("/addContact",methods=["GET","POST"])
def addContact():

	try:
		name = request.args.get("name", None)
		email = request.args.get("email",None)
		number = request.args.get("number",None)
		key = request.args.get("key",None)
		val = cursor.execute("SELECT * from contacts where email = (%s)",(email))
		if(name and email and number):
			val = cursor.execute("SELECT * from contacts where email = (%s)",(email))
			result = cursor.fetchall()
			print("len of Results ",len(result))
			if(len(result) >= 1):
				return "A contact with the email already exists"
			else:
				val = cursor.execute("INSERT INTO contacts (name,email,phonenumber)  VALUES (%s,%s,%s)",(name,email,number))
				db.commit()
				return "Contact Added Successfully"
		else:
			return "Please specify name,email and number by using the following url <b>http://localhost:5000/addContact?name=\"somename\"?email=\"Some email\"?number\"some number\"<b>"
	
	except:
		return "please check the given values"


#--------------------------------- Function for searching contacts by name -----------------------------------------------#
#by default page value is taken as 1 and for further contacts we should specify page value
@app.route("/searchContactByName",defaults={'page':1})
@app.route('/searchContactByName/<int:page>')
def searchContactByName(page):
	
	try:
		name = request.args.get("name",None)
		if(name):		
			val = cursor.execute("SELECT * from contacts where name like %s ",(name))
			allvalues = cursor.fetchall()
			print(page)
			limit = 10
			if(page == 1):
				start = 0
			elif(page >= 1 and (page-1)*limit <= len(allvalues) <= page*limit):
				start = (page-1)*limit
			else:
				return "no more to show"

			val = cursor.execute("SELECT * from contacts where name like %s limit %s,%s ",(name,start,limit))
			values = cursor.fetchall()
			if(len(values) >= 1):	
				str = ""
				#str += "Name  email  number"
				for x in values:
					str += "<b>Name</b> : "+x[0]+"  "
					str += "<b>Email</b> : "+x[1]+"  "
					str += "<b>Number</b> : "+x[2]+"<br/>"

				return str
			else:
				return "Contact with name"+name+"is not presnet"
		else:
			return "Please provide a valid name valid url is http://localhost:5000/searchContactByName?name=\"YourInputValue here\""

	except:	
		return "please check the input value"



#----------------------------------------- Function for searching contact by email ---------------------------------------------------------
#this does not require pagination because email is unique for each contacts for every email only one contact is assigned so for each email given we can have only one contact
@app.route("/searchContactByEmail")
def searchContactByEmail():
	try:
		email = request.args.get("email",None)
		#Condition for checking wether user has given input or not
		if(email):
			val = cursor.execute("SELECT * from contacts where email = (%s) ",(email))
			values = cursor.fetchall()
			if(len(values) >= 1):	
				str = ""
				for x in values:
					str += x[0]+"\t"
					str += x[1]+"\t"
					str += x[2]+"\n"
				return str
			else:
				return "Contact with email"+email+"is not presnet"
		else:
			return "Please provide a valid email valid url is http://localhost:5000/searchContactByEmail?email=YourInputValue here"
	
	except:	
		return "please check the input value"
    



@app.route("/deleteContact")
def deleteContact():
	return "You can Delete your contacts here"




if __name__ == "__main__":
	app.run(debug=True)
