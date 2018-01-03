from pymongo import MongoClient
from utils import get_llama_id
import random
import string

	

def get_llama(u):
	user_id = get_llama_id(u)		
	userdata = usersdb[user_id]
	llama = userdata["llama"]
	return llama
def edit_llama(u,llama):	
	user_id = get_llama_id(u)	
	userdata = usersdb[user_id]
	userdata["llama"] = llama
		
	

def get_userid_from_credentials(username,password):
	i = 1
	user_id = 0
	for u in usersdb:
		if u["user"] == username and u["pass"] == password:
			user_id = i
		i = i+1
	if user_id != 0 :
		return user_id
	return False


class LlamaDB :
	
	def __init__(self,name):
		self.client = MongoClient('mongo', 27017)
		self.name = name
		self.db = self.client[self.name]
		self.logged_users = {}
		collection_names = self.db.collection_names(include_system_collections=False)
		users = self.db.users
		#~ users.drop()
		user = self.get_user_from_credentials("pippo","pippo")
		if collection_names == [] :
			user = { "username" : "pippo" , "password" : "pippo" , "llamaSave" : None}
			user_id = users.insert_one(user).inserted_id
			
	def get_logged_llama_session_ids(self):
		return self.logged_users.keys()
	def logout_user(self,sessionID):
		self.logged_users.pop(sessionID,None)
	def generateNewRandomSessionString(self):
		N = 32
		s = ''.join(random.choice(string.ascii_lowercase + string.digits + "-") for _ in range(N))
		if s in self.logged_users.keys():
			return self.generateNewRandomSessionString()
		return s
	def login_user(self,user_id):
		if user_id == False : return False
		for sess_id, user in self.logged_users.iteritems() :
			if user["_id"] == user_id :
				return sess_id
		sess_id = self.generateNewRandomSessionString()
		user = self.get_user(user_id)
		print (str(user_id) + "xx")
		user["llama"] = None
		self.logged_users[sess_id] = user
		return sess_id
	def get_logged_user_id(self,sessionID):
		user = self.get_logged_user(sessionID)
		if user == False : return False
		return user["_id"]
	def get_logged_user(self,sessionID):
		for sess_id,user in self.logged_users.iteritems():
			if sess_id == sessionID :
				return user
		return False
	def set_logged_user(self,sessionID,user):
		if sessionID in self.logged_users.keys() :
			self.logged_users[sessionID] = user
			return True
		return False
	def get_user(self,user_id):
		users = self.db.users
		user = users.find_one({"_id": user_id})
		return user
		
	def get_user_id_from_credentials(self,username,password):
		user = self.get_user_from_credentials(username,password)
		if user == False : return False
		return user["_id"]
			
	def get_user_from_credentials(self,username,password):
		users = self.db.users
		user = users.find_one({"username": username, "password" : password})
		try:
			return user
		except KeyError :
			pass
		return False

	def loadLlama(self,user_id) :
		user = self.get_user(user_id)
		return user["llamaSave"]
	def saveLlama(self,llama,user_id) :
		data = llama.toJSON()
		user = self.get_user(user_id)
		user["llamaSave"] = data
		self.db.users.update_one({'_id':user_id}, {"$set": user}, upsert=False)
		
	def set_llama(self,user_id,llama) :
		sessionID = self.login_user(user_id)
		user = self.get_logged_user(sessionID)
		user["llama"] = llama
		return self.set_logged_user(sessionID,user)
		
		
	def user_has_savefile(self,user) :
		return not user["llamaSave"] == None 
	def get_llama(self,user_id) :
		sessionID = self.login_user(user_id)
		user = self.get_logged_user(sessionID)
		if user == False :
			llama = False
		elif user["llama"] == None :
			if self.user_has_savefile(user) :
				llama = "load"
			else :
				llama = "new"
		else :
			llama = user["llama"]
		return llama
			
		
