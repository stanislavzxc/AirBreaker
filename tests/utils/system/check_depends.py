import pytest

from utils.system import check_depends


@pytest.mark.asyncio
async def test_all_deps_present(monkeypatch):
    monkeypatch.setattr("shutil.which", lambda name: f"/usr/bin/{name}")

    wanted = ["ip", "iw", "iwlist"]
    missing = await check_depends(wanted)

    assert missing == []
