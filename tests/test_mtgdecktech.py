#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `mtgdecktech` package."""

import re
import pytest
from click.testing import CliRunner
from mtgdecktech import cli


@pytest.fixture
def response():
    """Sample pytest fixture.

    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    # import requests
    # return requests.get('https://github.com/audreyr/cookiecutter-pypackage')


def test_content(response):
    """Sample pytest test function with the pytest fixture as an argument."""
    # from bs4 import BeautifulSoup
    # assert 'GitHub' in BeautifulSoup(response.content).title.string


def test_command_line_interface():
    """Test the CLI."""
    runner = CliRunner()
    help_result = runner.invoke(cli.server, ['--help'])
    assert help_result.exit_code == 0
    assert re.search(r'--help\s+Show this message and exit\.',
                     help_result.output)
