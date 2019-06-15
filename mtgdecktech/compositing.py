#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (C) Metaswitch Networks.
"""Classes for compositing scenes."""

import logging
import os
from PIL import Image, ImageDraw, ImageFont
from typing import Tuple, Any

log = logging.getLogger(__name__)


class Scene(object):
    """An image on which layers can be composited.

    """
    def __init__(self, width: int, height: int, background_color:Tuple = (0, 0, 0, 0)):
        self.im = Image.new("RGBA", (width, height), background_color)
        self.layers = []
        self.rendered = False

    def set_background_color(self, color: Tuple):
        new_im = Image.new("RGBA", (self.im.width, self.im.height), color)
        self.im = new_im

    def add_layer(self, layer: 'Layer'):
        self.layers.append(layer)

    def save_to_file_object(self, f):
        im = self.im.copy()
        for layer in self.layers:
            layer.render(im)

        # Save the image to the file object
        im.save(f)

    def save(self, path: str):
        with open(path, "wb") as f:
            self.save_to_file_object(f)


class Layer(object):
    """A object which renders an image onto another image."""

    def render(self, base_im: Image):
        raise NotImplementedError

    def size(self, base_im: Image) -> Tuple[int, int]:
        raise NotImplementedError

    def position(self, base_im: Image, layer_im: Image) -> Tuple[int, int]:
        raise NotImplementedError


class CardLayer(Layer):
    """A layer consisting of a card image."""

    DEFAULT_SCALE = 0.6666

    def __init__(self, im: Image, height_scale: float = DEFAULT_SCALE):
        super(CardLayer, self).__init__()
        self.im = im
        self.height_scale = height_scale

    def size(self, base_im: Image) -> Tuple[int, int]:
        new_height_float = base_im.height * self.height_scale
        new_width_float = (self.im.width * new_height_float) / self.im.height
        return int(new_width_float), int(new_height_float)

    def position(self, base_im: Image, layer_im: Image) -> Tuple[int, int]:
        """Centers the layer image within the base image."""
        x_pos = int((base_im.width - layer_im.width) / 2)
        y_pos = int((base_im.height - layer_im.height) / 2)
        return x_pos, y_pos

    def render(self, base_im: Image):
        """Rescale the card image appropriately, then render."""

        new_size = self.size(base_im)

        if new_size[1] < self.im.height:
            # Use a high-quality downsampler
            resampler = Image.LANCZOS
        else:
            resampler = Image.NEAREST

        log.debug("[%s] Resizing card image from %s to %s",
                  self,
                  self.im.size,
                  new_size)
        resize_im = self.im.resize(new_size, resampler)

        # Get the position for the card.
        pos = self.position(base_im, resize_im)

        log.debug("[%s] Rendering to position %s", self, pos)
        base_im.paste(resize_im, pos, resize_im)

    @classmethod
    def from_image(cls, im: Image, height_scale: float = DEFAULT_SCALE) -> 'CardLayer':
        return cls(im, height_scale)


class SubtitleLayer(Layer):
    """A subtitle for an existing layer."""

    def __init__(self, attached_layer: Layer, subtitle: str, height_px: int):
        self.attached_layer = attached_layer
        self.subtitle = subtitle
        self.height_px = height_px

        # Create a font of the correct size.
        self.font_path = os.path.join(os.path.dirname(__file__),
                                      "static",
                                      "JaceBeleren-Bold.ttf")

        # Find a font size that will satisfy the width and height given.
        self.font_size = 0
        self.font = None

        test_font_size = 1
        test_font, calc_size = self._get_font_with_size(test_font_size)

        while calc_size[1] <= self.height_px:
            # Save off the current best font.
            self.font = test_font
            self.font_size = test_font_size
            test_font_size += 1
            test_font, calc_size = self._get_font_with_size(test_font_size)

        # Store off the size of the font bounding box.
        self.font_box = self.font.getsize(self.subtitle)

        log.debug("Actual rendering %r at font size %d => size %s",
                  self.subtitle,
                  self.font_size,
                  self.font_box)

        # self.im = Image.new("RGBA", (width, height), (0, 0, 0, 10))
        #
        #
        # d = ImageDraw.Draw(self.im)
        # d.text((0, 0), self.text, font=font, fill=(255, 255, 0))

    def render(self, base_im: Image):
        pass

        # base_im.paste(self.im,self.position(base_im, self.im), self.im)

    def size(self, base_im: Image):
        return self.font_box

    def position(self, base_im: Image, layer_im: Image) -> Tuple[int, int]:
        # return (0, 0)
        pass

    def _get_font_with_size(self, size: int) -> Tuple[Any, Tuple[int, int]]:
        font = ImageFont.truetype(self.font_path, size)
        text_size = font.getsize(self.subtitle)

        log.debug("Rendering %r at font size %d is size %s",
                  self.subtitle,
                  size,
                  text_size)

        return font, text_size


class DummyTextLayer(Layer):
    def __init__(self, text: str, width: int, height: int):
        self.text = text
        self.im = Image.new("RGBA", (width, height), (0, 0, 0, 10))
        self.font_path = os.path.join(os.path.dirname(__file__),
                                      "static",
                                      "JaceBeleren-Bold.ttf")

        # Find a font size that will satisfy the width and height given.
        font_size = 1
        font = None

        test_font, calc_size = self._get_font_with_size(font_size)

        while calc_size[0] <= width and calc_size[1] <= height:
            font = test_font
            font_size += 1
            test_font, calc_size = self._get_font_with_size(font_size)

        log.debug("Actual rendering %r at font size %d => size %s",
                  self.text,
                  font_size,
                  font.getsize(self.text))

        d = ImageDraw.Draw(self.im)
        d.text((0, 0), self.text, font=font, fill=(255, 255, 0))

    def render(self, base_im: Image):
        base_im.paste(self.im,self.position(base_im, self.im), self.im)

    def size(self, base_im: Image):
        return self.im.size

    def position(self, base_im: Image, layer_im: Image) -> Tuple[int, int]:
        return (0, 0)

    def _get_font_with_size(self, size: int) -> Tuple[Any, Tuple[int, int]]:
        font = ImageFont.truetype(self.font_path, size)
        text_size = font.getsize(self.text)

        log.debug("Rendering %r at font size %d is size %s",
                  self.text,
                  size,
                  text_size)

        return font, text_size
