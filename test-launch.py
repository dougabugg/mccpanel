import os, subprocess
os.environ["FLASK_APP"] = "mccpanel"
# os.spawnvp("python", ("-m", "flask", "run"))
subprocess.run(["python", "-m", "flask", "run"])
