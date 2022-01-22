import os, subprocess
os.environ["FLASK_APP"] = "mccpanel"
os.environ["MCCPANEL_CONFIG"] = "test_config.json"
subprocess.run(["python", "-m", "flask", "run"])
