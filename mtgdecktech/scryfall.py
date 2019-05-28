#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (C) Metaswitch Networks.
"""Interface to the scryfall_cache module"""

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import logging
from flask import g
from werkzeug.local import LocalProxy
import scryfall_cache

log = logging.getLogger(__name__)


def get_scryfall_cache():
    """Get an instance of the scryfall cache"""
    if not hasattr(g, 'scryfall'):
        log.debug("Creating new scryfall cache")
        g.scryfall = scryfall_cache.ScryfallCache("mtgdecktech")
    return g.scryfall
