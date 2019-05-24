# -*- coding: utf-8 -*-

"""Main module."""

from flask import Flask, request


app = Flask(__name__)


@app.route("/")
def main_page():
    """Render main page of the server.

    Returns:
        Page to render.

    """
    return "Hello world"


@app.route('/shutdown', methods=['POST'])
def shutdown():
    """Shutdown the Flask server without using Ctrl-C.

    Raises:
        RuntimeError: if not running inside Werkzeug Server for
                      some reason.

    Returns:
        Shutdown message.

    """
    # Use the recommended method from werkzeug to shutdown the server in
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
    return 'Server shutting down...'
