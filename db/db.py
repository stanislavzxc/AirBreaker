# SPDX-License-Identifier: GPL-3.0-or-later

from motor.motor_asyncio import AsyncIOMotorClient
import logging

logger = logging.getLogger(__name__)

class MongoDB():
    def __init__(self):
        self.client: AsyncIOMotorClient = None
        self.db = None

    async def open_connection(self, db_path: str, db_name: str) -> None:
        self.client = AsyncIOMotorClient(db_path)
        self.db = self.client[db_name]
        try:
            await self.db.command("ping")

        except Exception as e:
            logger.error(f"error with db", exc_info=e)
            raise e

    async def close_connection(self) -> None:
        if self.client:
            self.client.close()

db_repo = MongoDB()

def get_db():
    return db_repo.db
    
