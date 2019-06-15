#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (C) Metaswitch Networks.
"""Interface to the scryfall_cache module"""

import logging
from flask import g
from werkzeug.local import LocalProxy
from PIL import Image
from scryfall_cache import ScryfallCache

log = logging.getLogger(__name__)


def get_scryfall_cache() -> ScryfallCache:
    """Get an instance of the scryfall cache"""
    if not hasattr(g, 'scryfall'):
        log.debug("Creating new scryfall cache for request")
        g.scryfall = ScryfallCache("mtgdecktech")
    return g.scryfall


def close_scryfall_cache():
    """Closes an instance of the scryfall cache"""
    if hasattr(g, 'scryfall'):
        log.debug("Closing scryfall cache")
        g.scryfall.close()


scryfall_client = LocalProxy(get_scryfall_cache)  # type: ScryfallCache


class ImageGenerator(object):
    @staticmethod
    def from_mtgo_id(mtgo_id: int) -> Image:
        log.debug("Getting PIL image for MTGO ID %d", mtgo_id)
        card = scryfall_client.get_card(mtgo_id=mtgo_id)
        if not card:
            return None

        # Get the local image path. The PNG format gives a card image
        # with transparency.
        image_path = card.get_image_path("png")

        # Load the image with PIL
        im = Image.open(image_path).convert("RGBA")

        return im
