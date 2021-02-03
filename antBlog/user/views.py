# -*- coding: utf-8 -*-
"""User views."""
import flask
from flask import Blueprint, render_template
from flask_login import login_required
import flask_praetorian

from antblog.extensions import guard

blueprint = Blueprint("user", __name__, url_prefix="/users", static_folder="../static")


@blueprint.route("/")
@login_required
def members():
    """List members."""
    return render_template("users/members.html")


@blueprint.route("/login", methods=["POST"])
def login():
    """
    Logs a user in by parsing a POST request containing user credentials and
    issuing a JWT token.
    .. example::
       $ curl http://localhost:5000/login -X POST \
         -d '{"username":"Walter","password":"calmerthanyouare"}'
    """
    req = flask.request.get_json(force=True)
    username = req.get("username", None)
    password = req.get("password", None)
    user = guard.authenticate(username, password)
    ret = {"access_token": guard.encode_jwt_token(user)}
    return (flask.jsonify(ret), 200)


@blueprint.route("/protect", methods=["GET"])
@flask_praetorian.auth_required
def protect():
    """List members."""
    return "ye"
