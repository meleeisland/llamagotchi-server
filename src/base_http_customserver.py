"""Server Class with custom get/post and authentication"""
from BaseHTTPServer import BaseHTTPRequestHandler
from inspect import getargspec
import urlparse

import json

from src.llama_class import get_llama


def extract_json(val):
    """Return val[0] if val is a list of items, val if is unicode or int"""
    if isinstance(val, list):
        return val[0]
    if isinstance(val, (int, str)):
        return val
    return None


def execute_custom_fun(fun, llama, user_id, session_id):
    """Execute function fun that returns dict
    with optional arguments llama,user_id,session_id """
    data = {}
    sig = getargspec(fun).args
    parameters = []
    for _p in sig:
        if _p != "self":
            parameters.append(_p)
    try:
        if llama is None or not parameters:
            data = fun()
        elif len(parameters) == 1:
            data = fun(llama)
        elif len(parameters) == 2:
            data = fun(llama, user_id)
        elif len(parameters) == 3:
            data = fun(llama, user_id, session_id)
        return data
    except TypeError:
        return {"type": "error", "data": "suca"}


def execute_custom_fun_with_data(fun, llama, user_id, session_id, post_data):
    """Execute function fun that returns dict with argument post_data
     and optional arguments llama,user_id,session_id """
    data = {}
    sig = getargspec(fun).args
    parameters = []
    for _p in sig:
        if _p != "self":
            parameters.append(_p)
    if llama is None or (len(parameters) == 1):
        data = fun(post_data)
    elif len(parameters) == 2:
        data = fun(llama, post_data)
    elif len(parameters) == 3:
        data = fun(llama, user_id, post_data)
    elif len(parameters) == 4:
        data = fun(llama, user_id, session_id, post_data)
    return data


class BaseHTTPcustomServer(BaseHTTPRequestHandler):
    """Server Class with custom get/post and authentication"""

    def init_custom_server(self, init_args):
        """Initialize server from constructor function"""
        self.stored_post_data = {}
        self._db = init_args["database"]

    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    def do_HEAD(self):
        """HEAD response"""
        self._set_headers()

    def do_OPTIONS(self):
        """OPTIONS response"""
        self.send_response(200, "ok")
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header("Access-Control-Allow-Headers", "X-Requested-With")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def log(self, msg):
        """Log a message string"""
        BaseHTTPRequestHandler.log_message(self, msg)

    def auth_post_data(self):
        """Get session_id from postdata"""
        try:
            post_data = self.get_post_data()
            self.log(str(post_data))
            session_id = post_data["uid"]
            if session_id != None:
                return session_id
        except KeyError:
            pass
        return False

    def auth_query(self):
        """Get session_id from get query"""
        try:
            _p = urlparse.urlparse(self.path)
            _q = urlparse.parse_qs(_p.query)
            session_id = extract_json(_q["uid"])
            return session_id
        except KeyError:
            pass
        return False

    def get_post_data(self):
        """Get postdata and cache it"""
        content_length = int(self.headers['Content-Length'])
        content_type = (self.headers['Content-Type'])
        post_data = self.rfile.read(content_length)
        content_type = content_type.split(";")
        if "application/json" in content_type:
            self.stored_post_data = json.loads(post_data)
        else:
            self.stored_post_data = urlparse.parse_qs(post_data)
        return self.stored_post_data

    def get_stored_post_data(self):
        """Get cached post_data of a recent post request"""
        return self.stored_post_data

    def custom_get(self, fun):
        """Execute fun getting user_id,llama,session_id from query"""
        try:
            self._set_headers()
            session_id = self.auth_query()
            self.log(str(session_id))
            user_id = self._db.get_logged_user_id(session_id)
            llama, _ = get_llama(self._db, user_id)
        except KeyError:
            user_id = - 1
            llama = None
        data = execute_custom_fun(fun, llama, user_id, session_id)
        msg = json.dumps(data)
        self.wfile.write(msg)

    def custom_post(self, fun):
        """Execute fun with postdata getting user_id,llama,session_id from postdata"""
        try:
            self._set_headers()
            session_id = self.auth_post_data()
            user_id = self._db.get_logged_user_id(session_id)
            llama, _t = get_llama(self._db, user_id)
        except KeyError:
            user_id = - 1
            llama = None

        self.log(str(llama))
        self.log(str(user_id) + "u")
        self.log(str(session_id) + "s")
        data = execute_custom_fun_with_data(
            fun, llama, user_id, session_id, self.get_stored_post_data())
        msg = json.dumps(data)
        self.wfile.write(msg)
