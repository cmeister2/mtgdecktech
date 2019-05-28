# -*- coding: utf-8 -*-

"""Main module."""

from flask import Flask, request, render_template, abort, current_app, send_file, g
from .scryfall import get_scryfall_cache

app = Flask(__name__)


@app.route("/")
def main_page():
    """Render main page of the server.

    Returns:
        Page to render.

    """
    g.test = "Max"

    sc = get_scryfall_cache()
    return render_template("main_page.html", sc=sc)


@app.route('/mtgo/<int:mtgo_id>.jpg')
def render_image(mtgo_id: int):
    """Render image for given MTGO ID.

    Returns:
        Binary image data.

    """
    current_app.logger.info("Render card with MTGO ID %d", mtgo_id)

    current_app.logger.info("g: %s", g)
    current_app.logger.info("g.test: %s", g.test)
    current_app.logger.info("g.scryfall: %s", g.scryfall)

    sc = get_scryfall_cache()
    card = sc.get_card(mtgo_id=mtgo_id)
    if not card:
        # Failed to find the card
        abort(404)

    current_app.logger.debug("Card: %s", card)

    # Get the local image path for the image. This might download the image.
    image_path = card.get_image_path("png")
    current_app.logger.debug("Image path: %s", image_path)

    # Return the image data.
    return send_file(image_path, mimetype="image/png")


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
