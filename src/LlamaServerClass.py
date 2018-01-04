from BaseHTTPServer import HTTPServer

import urlparse

from src.LlamaClass import Llama
from src.base_http_customserver import BaseHTTPcustomServer,extract_json


from src.llama_db import LlamaDb


def MakeLlamaServerFromArgs(init_args):
    class LlamaCustomHTTP(BaseHTTPcustomServer, object):
        def __init__(self, *args, **kwargs):
            self.init_custom_server(init_args)
            super(LlamaCustomHTTP, self).__init__(*args, **kwargs)

        def check_login(self, data):
            ok = False
            try:
                if data["type"] == "login":
                    username = data["username"]
                    password = data["password"]
                    ok = self._db.get_user_id_from_credentials(username, password)
            except KeyError:
                pass
            return ok

        def do_GET(self):

            p = urlparse.urlparse(self.path)
            if p.path == "/ghappy/":
                self.custom_get(self.getHappiness)
            elif p.path == "/gname/":
                self.custom_get(self.getName)
            elif (p.path == "/keepalive/"):
                self.custom_get(self.getKeepalive)
            elif p.path == "/save/":
                self.custom_get(self.getSave)
            elif p.path == "/logout/":
                self.custom_get(self.getLogout)
            else:
                self.custom_get(self.getError)

        def getError(self):
            return {"type": "error", "data": "suca:nopath"}

        def getName(self, llama):
            name = ""
            try:
                if (llama != None):
                    name = llama.getName()
            except KeyError:
                pass
            if name != "":
                return {"type": "name", "data": name}
            return {"type": "error", "data": "suca"}

        def getKeepalive(self, llama):
            try:
                val = llama.keepAlive()
                return {"type": "keepalive", "data": val}
            except (KeyError, AttributeError) as error:
                return {"type": "keepalive", "data": "false"}

        def getHappiness(self, llama):
            happy = -1
            try:
                if (llama != False):
                    happy = llama.llamagotchi.getHappiness()
            except (KeyError, AttributeError) as error:
                pass
            if happy != -1:
                return {"type": "happiness", "data": happy}
            return {"type": "error", "data": "suca"}

        def getSave(self, llama, u):
            data = ""
            llama.save(u)
            if (llama != False):
                data = llama.getName() + " saved"
            if data != "":
                return {"type": "name", "data": data}
            return {"type": "error", "data": "suca"}

        def getLogout(self, llama, u, s):
            data = ""
            if u != False:
                llama.save()
                self.db.set_llama(u, None)
                self.db.logout_user(s)
                return {"type": "ok", "data": "bye!"}
            return {"type": "error", "data": "suca"}

        def do_POST(self):

            if (self.path == "/login/"):
                self.custom_post(self.postLogin)
            elif (self.path == "/pet/"):
                self.custom_post(self.postPet)
            elif (self.path == "/sname/"):
                self.custom_post(self.postSetName)
            elif (self.path == "/new/"):
                self.custom_post(self.postNew)
            else:
                self.custom_post(self.getError)

        def postNew(self, llama, u):
            self.set_llama(u, Llama(""))
            llama = self.get_llama(u)
            if (llama != None):
                return {"type": "ok",	"data":  "new llama : name <" + llama.getName() + ">"}
            return {"type": "error", "data": "suca"}

        def postSetName(self, llama, data):
            name = extract_json(data["name"])
            llama.setName(name)
            if (llama != None):
                return {"type": "ok",	"data":  "new name : name <" + llama.getName() + ">"}
            return {"type": "error", "data": "suca"}

        def postPet(self, llama, data):
            llama.llamagotchi.pet()
            return {"type": "ok",	"data":   "baah!"}

        def postLogin(self, data):
            login = self.check_login(data)
            self.log(str(login))
            if login != False:
                sessionID = self._db.login_user(login)
                llama, t = self.get_llama(login)
                return {"type": t, "data": llama.getName(), "uid": sessionID}
            return {"type": "error", "data": "suca"}

    return LlamaCustomHTTP


class LlamaServer:
    def __init__(self, address="0.0.0.0", port=8080, mongodb=None):
        self.address = address
        self.port = port
        if mongodb == None:
            mongodb = LlamaDb("test")
        S = MakeLlamaServerFromArgs({"database": mongodb})
        self.httpd = HTTPServer((self.address, self.port), S)

    def start(self):
        print 'Starting httpd...'
        self.httpd.serve_forever()
