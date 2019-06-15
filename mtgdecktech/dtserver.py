# -*- coding: utf-8 -*-

"""Main module."""

import tempfile
from flask import Flask, request, render_template, abort, current_app, send_file, g
from .scryfall import scryfall_client, close_scryfall_cache, ImageGenerator
from .compositing import Scene, CardLayer, DummyTextLayer, SubtitleLayer


app = Flask(__name__)


@app.route("/")
def main_page():
    """Render main page of the server.

    Returns:
        Page to render.

    """
    mtgo_id = 12345
    current_app.logger.info("Render card with MTGO ID %d", mtgo_id)

    card = ImageGenerator.from_mtgo_id(mtgo_id)
    if not card:
        # Failed to find the card
        abort(404)

    scene1 = Scene(1920, 1080)
    layer1 = CardLayer(card)
    scene1.add_layer(layer1)

    # Add a SubtitleLayer which is related positionally to the card layer
    text1 = SubtitleLayer(layer1, "Hello", 50)
    scene1.add_layer(text1)

    with tempfile.NamedTemporaryFile(suffix=".png", delete=True) as f:
        current_app.logger.info("Temporary file is at %s", f.name)
        scene1.save_to_file_object(f)

        # Return the image data.
        return send_file(f.name, mimetype="image/png")


@app.route('/mtgo/<int:mtgo_id>.png')
def render_image(mtgo_id: int):
    """Render image for given MTGO ID.

    Returns:
        Binary image data.

    """
    current_app.logger.info("Render card with MTGO ID %d", mtgo_id)

    card = scryfall_client.get_card(mtgo_id=mtgo_id)
    if not card:
        # Failed to find the card
        abort(404)

    current_app.logger.debug("Card: %s", card)

    # Get the local image path for the image. This might download the image.
    image_path = card.get_image_path("png")
    current_app.logger.debug("Image path: %s", image_path)

    # Return the image data.
    return send_file(image_path, mimetype="image/png")


@app.route('/scene')
def render_scene():
    """Render a scene according to input.

    Returns:
        Binary image data.

    """
    scene_args = request.args.get('args')
    current_app.logger.info("Args: %s", scene_args)

    # current_app.logger.info("Render card with MTGO ID %d", mtgo_id)
    #
    # card = scryfall_client.get_card(mtgo_id=mtgo_id)
    # if not card:
    #     # Failed to find the card
    #     abort(404)
    #
    # current_app.logger.debug("Card: %s", card)
    #
    # # Get the local image path for the image. This might download the image.
    # image_path = card.get_image_path("png")
    # current_app.logger.debug("Image path: %s", image_path)
    #
    # # Return the image data.
    # return send_file(image_path, mimetype="image/png")

    abort(403)


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


@app.teardown_appcontext
def teardown_client(_ctx):
    close_scryfall_cache()
