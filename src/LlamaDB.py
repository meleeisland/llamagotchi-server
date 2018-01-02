
from src.utils import get_llama_id

usersdb = [{"user":"pippo","pass":"pippo","llama" : None}]

	

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
