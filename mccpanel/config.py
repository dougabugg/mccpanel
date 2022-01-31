from typing import OrderedDict
from mccpanel.mcserver import McServer
import os, json
# this should not use globals, will fix eventually

class Config:
    def __init__(self, config_file=None):
        self.config_file = None
        self.secret_key = None
        self.settings = None
        self.userdb = None
        self.servers = None
        if config_file:
            self.config_file = config_file
            self.load_from_file()
    def load_from_file(self, config_file=None):
        if config_file:
            self.config_file = config_file
        else:
            config_file = self.config_file
        try:
            fh = open(config_file)
        except FileNotFoundError:
            self.create_default_config(config_file)
            fh = open(config_file)
        self.settings = json.load(fh)
        self.userdb = {}
        for entry in self.settings["registered_users"]:
            ukey = "user:" + entry["username"]
            userdb[ukey] = entry
        self.servers = OrderedDict()
        for entry in self.settings["servers"]:
            server = McServer(entry["name"], entry["jar_file"], entry["cwd"])
            if server.name in self.servers:
                server.name += "-2"
            self.server[server.name] = server
            if entry.get("autostart"):
                server.start()
    def create_default_config(self, config_file):
        try:
            fh = open(config_file, "w")
        except Exception as e:
            print(f"FATAL ERROR: unable to create config file named `{config_file}`.")
            raise e
        default_settings = {
            "registered_users": [{"username": "root", "password": "root"}],
            "servers": [{"name": "main", "jar_file": "server.jar", "cwd": "./servers/main", "autostart": True}]
        }
        json.dump(default_settings, fh)

settings = None
userdb = None
servers = None

def init_from_settings():
    global settings, userdb, servers
    userdb = {}
    for entry in settings["registed_users"]:
        ukey = "user:" + entry["username"]
        userdb[ukey] = entry
    servers = OrderedDict()
    for entry in settings["servers"]:
        server = McServer(entry["name"], entry["jar_file"], entry["cwd"])
        servers[server.name] = server
        if entry.get("autostart"):
            server.start()

def load_user(username):
    global settings, userdb, servers
    return userdb.get(f"user:{username}")

def reload_config():
    global settings, userdb, servers
    config_file = open(os.environ["MCCPANEL_CONFIG"])
    settings = json.load(config_file)
    print("loading",settings)
    init_from_settings()

reload_config()
