# SPDX-License-Identifier: GPL-3.0-or-later

import re

import pytest

from utils.network import generate_random_mac


def test_is_work():
    mac : str = generate_random_mac()

    assert len(mac) == 17
    assert re.match(r"^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$", mac) is not None
