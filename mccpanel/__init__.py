from mccpanel import auth, cpanel
import flask

app = flask.Flask(__name__)
app.register_blueprint(auth)
app.register_blueprint(cpanel)
