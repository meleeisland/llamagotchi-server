"""Module for llamaserver"""
from BaseHTTPServer import HTTPServer

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
                    user_id = self._db.get_user_id_from_credentials(
                        username, password)
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
            if user_id != False:
                llama.save()
                set_llama(self._db, user_id, None)
                self._db.logout_user(session_id)
                return {"type": "ok", "data": "bye!"}
            return {"type": "error", "data": "suca"}

        def do_POST(self):
            """Do post request"""

            if self.path == "/login/":
                self.custom_post(self.post_login)
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
                return {"type": "ok",	"data":  "new llama : name <" + llama.get_name() + ">"}
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
            if login != False:
                session_id = self._db.login_user(login)
                llama, _t = get_llama(self._db, login)
                return {"type": _t, "data": llama.get_name(), "uid": session_id}
            return {"type": "error", "data": "suca"}

    return LlamaCustomHTTP


class LlamaServer(object):
    """Class for custom httpserver"""

    def __init__(self, address="0.0.0.0", port=8080, mongodb=None):
        self.address = address
        self.port = port
        if mongodb is None:
            mongodb = LlamaDb("test")
        self.request_handler = make_llamaserver_from_args({"database": mongodb})
        self.httpd = HTTPServer((self.address, self.port), self.request_handler)

    def start(self):
        """Start server"""
        print 'Starting httpd...'
        self.httpd.serve_forever()
