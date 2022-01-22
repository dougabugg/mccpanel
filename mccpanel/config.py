from typing import OrderedDict
from mccpanel.mcserver import McServer
import os, json
# this should not use globals, will fix eventually


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
