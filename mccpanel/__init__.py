from mccpanel import auth, cpanel
import flask

app = flask.Flask(__name__)
# TODO SECRET_KEY should be set from config file (ie, not in this repo)
app.config.from_mapping(SECRET_KEY="dev")
app.register_blueprint(auth.bp)
app.register_blueprint(cpanel.bp)
app.add_url_rule("/", endpoint="index")
