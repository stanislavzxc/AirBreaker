# SPDX-License-Identifier: GPL-3.0-or-later

from unittest.mock import AsyncMock

from utils.system.run_command import run_command


class FakeProcess:
    def __init__(self, stdout: bytes = b"", stderr: bytes = b"", returncode: int = 0):
        self._stdout = stdout
        self._stderr = stderr
        self._returncode = returncode
        self.returncode = None

    async def communicate(self):
        self.returncode = self._returncode
        return self._stdout, self._stderr


async def test_success(monkeypatch):
    monkeypatch.setattr(
        "asyncio.create_subprocess_exec",
        AsyncMock(return_value=FakeProcess(b"ok\n", b"", 0)),
    )

    rc, out, err = await run_command("echo", "ok")

    assert rc == 0
    assert out == "ok"
    assert err == ""


async def test_failure(monkeypatch):
    monkeypatch.setattr(
        "asyncio.create_subprocess_exec",
        AsyncMock(return_value=FakeProcess(b"", b"boom\n", 1)),
    )

    rc, out, err = await run_command("false")

    assert rc == 1
    assert out == ""
    assert err == "boom"


async def test_strips_whitespace(monkeypatch):
    monkeypatch.setattr(
        "asyncio.create_subprocess_exec",
        AsyncMock(return_value=FakeProcess(b"   spaced   \n", b"  err  \n", 0)),
    )

    rc, out, err = await run_command("whatever")

    assert out == "spaced"
    assert err == "err"


async def test_empty_output(monkeypatch):
    monkeypatch.setattr(
        "asyncio.create_subprocess_exec",
        AsyncMock(return_value=FakeProcess(b"", b"", 0)),
    )

    rc, out, err = await run_command("true")

    assert (rc, out, err) == (0, "", "")


async def test_invalid_utf8_is_replaced(monkeypatch):
    monkeypatch.setattr(
        "asyncio.create_subprocess_exec",
        AsyncMock(return_value=FakeProcess(b"\xff\xfe", b"", 0)),
    )

    rc, out, err = await run_command("whatever")

    assert "\ufffd" in out
    assert rc == 0

