# SPDX-License-Identifier: GPL-3.0-or-later
import os

from asyncio import to_thread


def sync_get_wifi_chipsets():
    interfaces = []
    main_dir = "/sys/class/net/"

    if not os.path.exists(main_dir):
        return {"success": False, "message": "sys/class/net dir doesnt exist, maybe not a linux?" }
    
    for iface in os.listdir(main_dir):
        wifi_dir = os.path.join(main_dir, iface, "wireless")
        phy_symlink = os.path.join(main_dir, iface, "phy80211")
        
        if os.path.exists(wifi_dir) or os.path.exists(phy_symlink):
            try:
                with open(os.path.join(main_dir, iface, "operstate"), "r") as f:
                    state = f.read().strip()
            except:
                state = "unknown"

            interfaces.append({
                "interface": iface,
                "state": state,
                "driver": os.path.basename(os.readlink(os.path.join(main_dir, iface, "device", "driver"))) if os.path.exists(os.path.join(main_dir, iface, "device", "driver")) else "unknown"
            })
            
    return interfaces

async def get_wifi_chipset():
    return await to_thread(sync_get_wifi_chipsets)