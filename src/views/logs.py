from flask import render_template, redirect, Blueprint, flash
from flask import current_app as app
import helper

from logger.logger import Logger

log = Blueprint("logs", __name__)


@log.route("/logs")
def logs():
    if not helper.logged_in():
        flash("Log in to use the application", "error")
        return redirect("/")

    logs = Logger().read_all_events()
    logs.reverse()
    
    return render_template("logs/logs.html", logs=logs, reverse=False)

@log.route("/logs/oldestfirst")
def logs_reversed():
    if not helper.logged_in():
        flash("Log in to use the application", "error")
        return redirect("/")

    logs = Logger().read_all_events()
    
    return render_template("logs/logs.html", logs=logs, reverse=True)
