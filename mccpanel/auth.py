from mccpanel import config
import flask, functools

bp = flask.Blueprint("auth", __name__, url_prefix="/auth")

# adapted from https://github.com/pallets/flask/blob/2.0.2/examples/tutorial/flaskr/auth.py
def login_required(view):
    """view decorator for requiring authentication"""
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if flask.g.user is None:
            return flask.redirect(flask.url_for("auth.login"))
        return view(**kwargs)
    return wrapped_view

@bp.before_app_request
def load_logged_in_user():
    username = flask.session.get("username")
    if username is None:
        flask.g.user = None
    else:
        flask.g.user = config.load_user(username)

@bp.route("/login", methods=("GET", "POST"))
def login():
    req = flask.request
    if req.method == "POST":
        username = req.form["username"]
        passtoken = req.form["passtoken"]
        error = None
        user = config.load_user(username)
        if user is None:
            error = "invalid username"
        elif user.get("passtoken") != passtoken:
            error = "invalid passtoken"
        if error is None:
            flask.session.clear()
            flask.session["username"] = username
            return flask.redirect(flask.url_for("index"))
        flask.flash(error)
    return flask.render_template("auth_login.html")

@bp.route("/logout")
def logout():
    flask.session.clear()
    return flask.redirect(flask.url_for("index"))
