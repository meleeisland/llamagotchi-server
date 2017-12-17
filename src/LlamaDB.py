
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
		
	
