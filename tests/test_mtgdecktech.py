#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `mtgdecktech` package."""

import re
from click.testing import CliRunner
import mtgdecktech
from mtgdecktech.cli import server, app


def test_command_line_interface():
    """Test the CLI."""
    runner = CliRunner()
    help_result = runner.invoke(server, ['--help'])
    assert help_result.exit_code == 0
    assert re.search(r'--help\s+Show this message and exit\.',
                     help_result.output)


def test_scene():
    scene = mtgdecktech.Scene(1920, 1080)
    with app.app_context():
        card_image = mtgdecktech.ImageGenerator.from_mtgo_id(12345)

    # Create a card layer
    cl = mtgdecktech.CardLayer.from_image(card_image)
    scene.add_layer(cl)

    # Now create a subtitle layer for the card layer.
    subtitle = mtgdecktech.SubtitleLayer(cl, "4", "Times New Roman", 36)
    scene.add_layer(subtitle)

    scene.set_background_color((204, 241, 255))
    scene.save("/tmp/scene.png")
