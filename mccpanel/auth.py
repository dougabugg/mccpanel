from mccpanel import config
import flask, functools

bp = flask.Blueprint("auth", __name__, url_prefix="/auth")

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
    passtoken = flask.session.get("passtoken")
    if username is None or passtoken is None:
        flask.g.user = None
    else:
        pass
