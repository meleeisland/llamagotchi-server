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
	uid = None
	i = 0
	for k,u in users.iteritems() :
		if u == user_id :
			uid = i
		i = i + 1
	if uid == None :
		uid = len(users)
		users[uid] = user_id 
	return uid

def get_llama_id(u):		
	global users
	user_id = users[u-1] - 1
	return user_id
	
	

def get_llamas_ids():	
	global users
	return map( lambda x : x +1 ,users.keys())
	
def userid_in_users(userid):
	global users
	if userid - 1 in users.keys() :
		return True
	else: return False
	
