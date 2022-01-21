from mccpanel import config, auth
import flask

bp = flask.Blueprint("cpanel", __name__)

@bp.route("/")
@auth.login_required
def index():
    servers = list(config.servers.values())
    return flask.render_template("cpanel_index.html", servers=servers)

@bp.route("/server/<name>/")
@auth.login_required
def view_server(name):
    server = config.servers.get(name)
    if server is None:
        flask.flash("unknown server name")
        return flask.redirect(flask.url_for("cpanel.index"))
    return flask.render_template("cpanel_view_server.html", server=server)

@bp.route("/server/<name>/start")
def start(name):
    server = config.servers.get(name)
    if server is not None:
        server.start()
        return server.pid
    else:
        return "unknown server"

@bp.route("/server/<name>/output/<int:ts>")
def get_output(name, ts):
    server = config.servers.get(name)
    if server is not None:
        return flask.json.jsonify(server.get_output(ts))
    else:
        return "unknown server"

@bp.route("/server/<name>/input/<cmd>")
def put_input(name, cmd):
    server = config.servers.get(name)
    if server is not None:
        server.put_input(cmd)
        return "sent"
    else:
        return "unknown server"