"""Module for llamaserver"""
from BaseHTTPServer import HTTPServer

import thread
import time
import urlparse

from src.llama_class import Llama, get_llama, set_llama
from src.base_http_customserver import BaseHTTPcustomServer, extract_json


from src.llama_db import LlamaDb


def get_error():
    """Return errordata"""
    return {"type": "error", "data": "suca:nopath"}


def make_llamaserver_from_args(init_args):
    """Class Factory for BaseHTTPcustomServer::LlamaCustomHTTP"""
    class LlamaCustomHTTP(BaseHTTPcustomServer, object):
        """Class LlamaCustomHTTP for llamaserver custom requests"""

        def __init__(self, *args, **kwargs):
            self.init_custom_server(init_args)
            super(LlamaCustomHTTP, self).__init__(*args, **kwargs)

        def check_login(self, data):
            """Check postdata dict for login request return user_id, false on error"""
            user_id = False
            try:
                if data["type"] == "login":
                    username = data["username"]
                    password = data["password"]
                    user_id = str(
                        self._db.get_user_id_from_credentials(username, password))
                    self.log(user_id)
            except KeyError:
                pass
            return user_id

        def do_GET(self):
            """Do get request"""

            _p = urlparse.urlparse(self.path)
            if _p.path == "/ghappy/":
                self.custom_get(self.get_happiness)
            elif _p.path == "/gname/":
                self.custom_get(self.get_name)
            elif _p.path == "/keepalive/":
                self.custom_get(self.get_keepalive)
            elif _p.path == "/save/":
                self.custom_get(self.get_save)
            elif _p.path == "/logout/":
                self.custom_get(self.get_logout)
            else:
                self.custom_get(get_error)

        def get_name(self, llama):
            """From llama return llama name"""
            name = ""
            try:
                if llama != None:
                    name = llama.get_name()
            except KeyError:
                pass
            if name != "":
                return {"type": "name", "data": name}
            return {"type": "error", "data": "suca"}

        def get_keepalive(self, llama):
            """Reset keepalive count for llama"""
            try:
                val = llama.keep_alive()
                return {"type": "keepalive", "data": val}
            except (KeyError, AttributeError) as _:
                return {"type": "keepalive", "data": "false"}

        def get_happiness(self, llama):
            """From llama return llama happiness"""
            happy = -1
            try:
                if llama != False:
                    happy = llama.llamagotchi.get_happiness()
            except (KeyError, AttributeError) as _:
                pass
            if happy != -1:
                return {"type": "happiness", "data": happy}
            return {"type": "error", "data": "suca"}

        def get_save(self, llama, user_id):
            """Save llama on user with user_id"""
            data = ""
            llama.save(user_id)
            if llama != False:
                data = llama.get_name() + " saved"
            if data != "":
                return {"type": "name", "data": data}
            return {"type": "error", "data": "suca"}

        def get_logout(self, llama, user_id, session_id):
            """Logout user with session_id"""
            if session_id != False:
                llama.save()
                set_llama(self._db, user_id, None)
                self._db.logout_user(session_id)
                return {"type": "ok", "data": "bye!"}
            return {"type": "error", "data": "suca"}

        def do_POST(self):
            """Do post request"""

            if self.path == "/login/":
                self.custom_post(self.post_login)
            elif self.path == "/register/":
                self.custom_post(self.post_register)
            elif self.path == "/pet/":
                self.custom_post(self.post_pet)
            elif self.path == "/sname/":
                self.custom_post(self.post_set_name)
            elif self.path == "/new/":
                self.custom_post(self.post_new)
            else:
                self.custom_post(get_error)

        def post_new(self, llama, user_id, data):
            """Create new llama and set it to user_id"""
            set_llama(self._db, user_id, Llama(""))
            llama = get_llama(self._db, user_id)
            if llama != None:
                return {"type": "ok", "data":  "new llama : name <" + llama.get_name() + ">"}
            return {"type": "error", "data": "suca"}

        def post_register(self, data):
            """Add user to database with data.username, data.password"""
            try:
                username = data["username"]
                password = data["password"]
                user_id = self._db.get_user_id_from_credentials(
                    username, password)
                if user_id is not False:
                    return {"type": "error", "data":  "already exist"}
                user = self._db.add_user(username, password)
                return {"type": "ok", "data":  "new user : <" + str(user.inserted_id) + ">"}
            except KeyError:
                pass
            return {"type": "error", "data": "suca"}

        def post_set_name(self, llama, data):
            """Set name to llama"""
            name = extract_json(data["name"])
            llama.set_name(name)
            if llama != None:
                return {"type": "ok",	"data":  "new name : name <" + llama.get_name() + ">"}
            return {"type": "error", "data": "suca"}

        def post_pet(self, llama, data):
            """Pet llama"""
            llama.llamagotchi.pet()
            return {"type": "ok",	"data":   "baah!"}

        def post_login(self, data):
            """Check login and return llama if exist, ew error"""
            login = self.check_login(data)
            self.log("A:" + str(login))
            if login != False:
                session_id = self._db.login_user(login)
                self.log("S:" + str(session_id))
                llama, _t = get_llama(self._db, login)
                return {"type": _t, "data": llama.get_name(), "uid": session_id}
            return {"type": "error", "data": "suca"}

    return LlamaCustomHTTP


def default_llamaserver_config():
    """Return default config dict for llamaserver"""
    return {
        "delay": 1,
        "ticks": 1
    }


class LlamaServer(object):
    """Class for custom httpserver"""

    def __init__(self, address="0.0.0.0", port=8080, mongodb=None, config=None):
        self.address = address
        self.port = port
        if config is None:
            config = default_llamaserver_config()
        self.configure(config)
        if mongodb is None:
            mongodb = LlamaDb("test")
        self._db = mongodb
        self.request_handler = make_llamaserver_from_args(
            {"database": mongodb})
        self.httpd = HTTPServer(
            (self.address, self.port), self.request_handler)

    def configure(self, config):
        """Apply config dict"""
        self.delay = config["delay"]
        self.ticks = config["ticks"]

    def tick(self, thread_name, _delay, _max):
        """TickThread for time"""
        count = 0
        while True:
            time.sleep(_delay)
            llama_ids = self._db.get_logged_llama_session_ids()
            llamas = {}
            id_to_remove = []
            for session_id in llama_ids:
                user_id = self._db.get_logged_user_id(session_id)
                llama, _ = get_llama(self._db, user_id)
                llamas[session_id] = llama
            for _ in range(0, _max):
                print "[" + thread_name + "]" + "tick"
                count += 1
                for session_id in id_to_remove:
                    llamas.pop(session_id, None)
                for session_id, llama in llamas.iteritems():
                    if llama.tick() is False:
                        llama.save(user_id)
                        self._db.logout_user(session_id)
                        id_to_remove.append(session_id)

    def start_tick_thread(self):
        """Start ticking with current configuration"""
        try:
            thread.start_new_thread(
                self.tick, ("tick_thread", self.delay, self.ticks))
        except thread.error:
            print "Error: unable to start thread"

    def start(self):
        """Start server"""
        print 'Starting httpd...'
        self.start_tick_thread()
        self.httpd.serve_forever()
