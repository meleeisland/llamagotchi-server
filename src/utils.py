
import json
def unpack_dict(data):
	data = json.loads(data)
	type = data[0]
	values = data[1]
	user = data[2]
	return type,values,user
def pack_dict(t,m,u) :
	d = [t,m,u]
	a = json.dumps(d)	
	return a,len(a)

users = {}

def savefile_name(u):
	global users
	return "save-" + str(users[u-1] -1) +".json"
def remove_from_users(u):
	global users
	
	users.pop(u-1, None)
def add_to_users(user_id):
	global users
	uid = len(users)
	users[uid] = user_id 
	return uid

def get_llama_id(u):		
	global users
	user_id = users[u-1] - 1
	return user_id
	
	
	



	
def clean_request(data):
	if len(data) == 0 : return False
	return True
def logged_request(data):
	global users
	print data
	type,userdata,userid = unpack_dict(data)
	if userid - 1 in users.keys() :
		return True
	else: return False
