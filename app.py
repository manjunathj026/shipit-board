import os
import socket
from datetime import datetime, timezone

from flask import Flask, jsonify, redirect, render_template, request, url_for

import config

app = Flask(__name__)

# Notes live in memory, so they vanish when the app restarts.
# That is deliberate: in the Kubernetes phase you will see why
# real apps keep state in a database, not inside the container.
notes = []
MAX_NOTE_LENGTH = 120

STARTED_AT = datetime.now(timezone.utc).strftime("%d %b %Y %H:%M UTC")


def build_info():
    """Facts about this running copy of the app.

    The pipeline injects APP_VERSION, GIT_SHA and ENVIRONMENT as
    environment variables. Locally they fall back to defaults.
    """
    return {
        "version": os.getenv("APP_VERSION", "dev"),
        "commit": os.getenv("GIT_SHA", "local")[:7],
        "environment": os.getenv("ENVIRONMENT", "laptop"),
        "host": socket.gethostname(),  # in Kubernetes this is the pod name
        "started_at": STARTED_AT,
    }


@app.get("/")
def home():
    return render_template(
        "index.html",
        info=build_info(),
        message=config.MESSAGE,
        accent=config.ACCENT,
        notes=notes,
    )


@app.post("/notes")
def add_note():
    text = request.form.get("text", "").strip()[:MAX_NOTE_LENGTH]
    if text:
        notes.append(text)
    return redirect(url_for("home"))


@app.get("/health")
def health():
    # Docker, load balancers and Kubernetes probes call this.
    return jsonify(status="ok")


@app.get("/api/info")
def api_info():
    return jsonify(build_info())
