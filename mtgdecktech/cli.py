# -*- coding: utf-8 -*-

"""Console script for mtgdecktech."""
import logging
import os
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
        debug: Whether to enable debugging.

    Returns:
        Exit code for CLI.

    """
    if debug:
        # Check whether to start the browser. On initial start,
        # WERKZEUG_RUN_MAIN is None. On debug reload, this is now set.
        start_browser = os.environ.get("WERKZEUG_RUN_MAIN") is None
        logging_level = logging.DEBUG
    else:
        start_browser = True
        logging_level = logging.INFO

    # Configure logging
    logging.basicConfig(format="%(asctime)s %(levelname)-5.5s %(message)s",
                        stream=sys.stdout,
                        level=logging_level)

    if start_browser:
        # Start the browser asynchronously
        logging.info("Starting browser in thread...")
        url = "http://{host}:{port}".format(host=host, port=port)
        threading.Timer(1.25, lambda: webbrowser.open(url)).start()

    # Now start the application server.
    click.echo("Starting server")
    app.run(host=host, port=port, debug=debug)
    return 0


if __name__ == "__main__":
    sys.exit(server())  # pragma: no cover
