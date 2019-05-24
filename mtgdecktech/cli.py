# -*- coding: utf-8 -*-

"""Console script for mtgdecktech."""
import sys
import threading
import webbrowser
from mtgdecktech import app

import click


@click.command()
@click.option("--host", default="127.0.0.1", help="What IP to bind to")
@click.option("--port", default="5000", help="What port to bind to")
@click.option("--debug", default=False, help="Enable Flask debugging")
def server(host, port, debug):
    """Start server and pop up a webbrowser.

    Args:
        host: Which system IP to bind the web server to.
        port: Which port to expose the web server on.
        debug: Whether to enable Flask debugging.

    Returns:
        Exit code for CLI.

    """
    # Start the browser asynchronously
    click.echo("Start browser in thread")
    url = "http://{host}:{port}".format(host=host, port=port)
    threading.Timer(1.25, lambda: webbrowser.open(url)).start()

    # Now start the application server.
    click.echo("Starting server")
    app.run(host=host, port=port, debug=debug)
    return 0


if __name__ == "__main__":
    sys.exit(server())  # pragma: no cover
