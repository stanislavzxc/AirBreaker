# SPDX-License-Identifier: GPL-3.0-or-later

import os

from utils.network.network_card import get_wifi_chipsets


async def test_get_wifi_chipset_success(fs):
    fs.create_dir("/sys/class/net/wlan0/wireless")
    fs.create_file("/sys/class/net/wlan0/operstate", contents="up\n")

    driver_link = "/sys/class/net/wlan0/device/driver"
    fs.create_dir("/sys/bus/pci/drivers/ath10k_pci")
    fs.create_symlink(driver_link, "/sys/bus/pci/drivers/ath10k_pci")

    fs.create_dir("/sys/class/net/eth0")
    fs.create_file("/sys/class/net/eth0/operstate", contents="down\n")

    result = await get_wifi_chipsets()

    assert isinstance(result, list)
    assert len(result) == 1
    assert result[0]["interface"] == "wlan0"
    assert result[0]["state"] == "up"
    assert result[0]["driver"] == "ath10k_pci"

async def test_get_wifi_chipset_not_linux(fs):

    result = await get_wifi_chipsets()

    assert isinstance(result, dict)
    assert result["success"] is False
    assert "dir doesnt exist" in result["message"]
