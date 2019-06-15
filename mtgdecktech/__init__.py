# -*- coding: utf-8 -*-

"""Top-level package for mtgdecktech."""

__author__ = """Max Dymond"""
__email__ = 'cmeister2@gmail.com'
__version__ = '0.1.0'


from .dtserver import app  # noqa
from .compositing import Scene, CardLayer, SubtitleLayer  # noqa
from .scryfall import ImageGenerator  # noqa
