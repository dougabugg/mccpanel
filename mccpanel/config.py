from typing import OrderedDict
from mccpanel.mcserver import McServer

# eventually, this will be loaded from a JSON file, but for now, just hardcode a python dict

settings = {
    "registed_users": [
        {"username": "bunnmom", "passtoken": "cookie"}
    ],
    "servers": [
        {
            "name": "main",
            "jar_file": "paper-1.18.1-164.jar",
            "cwd": "./paper-server-01",
            # "autostart": True
        }
    ]
}

userdb = {}
for entry in settings["registed_users"]:
    ukey = "user:" + entry["username"]
    userdb[ukey] = entry

def load_user(username):
    return userdb.get(f"user:{username}")

servers = OrderedDict()
for entry in settings["servers"]:
    server = McServer(entry["name"], entry["jar_file"], entry["cwd"])
    servers[server.name] = server
    if entry.get("autostart"):
        server.start()

def reload_config():
    # TODO
    pass
