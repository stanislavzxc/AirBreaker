# SPDX-License-Identifier: GPL-3.0-or-later

from motor.motor_asyncio import AsyncIOMotorClient

class MongoDb():
    def __init__(self):
        self.client: AsyncIOMotorClient = None
        self.db = None

    def open_connection(self, db_path: str, db_name: str) -> None:
        self.client = AsyncIOMotorClient(db_path)
        self.db = self.client(db_name)
    
    def close_connection(self) -> None:
        if self.client:
            self.client.close()

db_repo = MongoDb()

def get_db():
    return db_repo.db
    