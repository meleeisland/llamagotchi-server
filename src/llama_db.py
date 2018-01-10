"""Module for database query with mongo."""
import random
import string
from pymongo import MongoClient
from bson.objectid import ObjectId

def user_has_savefile(user):
    """Return bool if savefile exist for user array"""
    return not user["llamaSave"] is None


class LlamaDb(object):
    """Class for database query with mongo."""

    def __init__(self, name):
        self.client = MongoClient('mongo', 27017)
        self.name = name
        self._db = self.client[self.name]
        self.logged_users = {}
        collection_names = self._db.collection_names(
            include_system_collections=False)
        if collection_names == []:
            _ = self.add_user("pippo", "pippo")
            
    def add_user(self, username, password):
        """Add an user to mongodb"""
        users = self._db.users
        user = {"username": username, "password": password, "llamaSave": None}
        user_id = users.insert_one(user)
        return user_id

    def get_logged_llama_session_ids(self):
        """Return an array with all session IDs"""
        return self.logged_users.keys()

    def logout_user(self, session_id):
        """Remove user with session_id from logged users"""
        self.logged_users.pop(session_id, None)

    def new_random_session_string(self):
        """Generate random string of 32 char with lowercase digits and hypen """
        __n = 32
        __s = ''.join(
            random.choice(string.ascii_lowercase + string.digits + "-") for _ in range(__n)
        )
        if __s in self.logged_users.keys():
            return self.new_random_session_string()
        return __s

    def login_user(self, user_id):
        """Add user with user_id to logged users and return session_id"""
        if user_id is False:
            return False
        for sess_id, user in self.logged_users.iteritems():
            if str(user["_id"]) == str(user_id):
                return sess_id
        sess_id = self.new_random_session_string()
        user = self.get_user(user_id)
        with open(".logs", "a") as myfile:
            myfile.write(str(user))
        user["llama"] = None
        self.logged_users[sess_id] = user
        return sess_id

    def get_logged_user_id(self, session_id):
        """Get user_id from user with session_id"""
        user = self.get_logged_user(session_id)
        if user is False:
            return False
        return user["_id"]

    def get_logged_user(self, session_id):
        """Get user array from user with session_id"""
        for sess_id, user in self.logged_users.iteritems():
            if sess_id == session_id:
                return user
        return False

    def set_logged_user(self, session_id, user):
        """Set user array for user with session_id as user"""
        if session_id in self.logged_users.keys():
            self.logged_users[session_id] = user
            return True
        return False

    def get_user(self, user_id):
        """Get user with user_id"""
        users = self._db.users
        user = users.find_one({"_id": ObjectId(user_id)})
        return user

    def get_user_id_from_credentials(self, username, password):
        """Get user_id with username : password """
        user = self.get_user_from_credentials(username, password)
        if user is False:
            return False
        return user["_id"]

    def get_user_from_credentials(self, username, password):
        """Get user array with username : password """
        users = self._db.users
        user = users.find_one({"username": username, "password": password})
        try:
            return user
        except KeyError:
            pass
        return False

    def load_llama(self, user_id):
        """ Get user savedata from user with user_id """
        user = self.get_user(user_id)
        return user["llamaSave"]

    def save_llama(self, llama, user_id):
        """ Set user savedata from llama to user with user_id """
        data = llama.to_json()
        user = self.get_user(user_id)
        user["llamaSave"] = data
        self._db.users.update_one(
            {'_id': user_id}, {"$set": user}, upsert=False)

    def set_llama(self, user_id, llama):
        """ Set current llama to llama to user with user_id """
        session_id = self.login_user(user_id)
        user = self.get_logged_user(session_id)
        user["llama"] = llama
        return self.set_logged_user(session_id, user)

    def get_llama(self, user_id):
        """ Get current llama from user with user_id """
        session_id = self.login_user(user_id)
        user = self.get_logged_user(session_id)
        if user is False:
            llama = False
        elif user["llama"] is None:
            if user_has_savefile(user):
                llama = "load"
            else:
                llama = "new"
        else:
            llama = user["llama"]
        return llama
