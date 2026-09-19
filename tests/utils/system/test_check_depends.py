# SPDX-License-Identifier: GPL-3.0-or-later

from utils.system import check_depends


async def test_all_deps_present(monkeypatch):
    monkeypatch.setattr("shutil.which", lambda name: f"/usr/bin/{name}")

    wanted = ["ip", "iw", "iwlist"]
    missing = await check_depends(wanted)

    assert missing == []

async def test_nothing_deps_present(monkeypatch):
    monkeypatch.setattr("shutil.which", lambda name: None)

    wanted = ["ip", "iw", "iwlist"]
    missing = await check_depends(wanted)

    assert missing == wanted

async def test_patrial_deps_present(monkeypatch):
    wanted = ["ip", "iw", "iwlist"]
    installed = ["ip"]

    monkeypatch.setattr("shutil.which", lambda name: f"/usr/bin/{name}" if name in installed else None)

    missing = await check_depends(wanted)

    assert missing == ["iw", "iwlist"]
    
async def test_is_duplicat(monkeypatch):
    wanted = ["ip", "ip", "iwlist"]
    monkeypatch.setattr("shutil.which", lambda name: None)

    missing = await check_depends(wanted)

    assert missing == ["ip", "iwlist"]
