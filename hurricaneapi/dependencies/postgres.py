from typing import Any, Optional

import asyncpg

from hurricaneapi.dependencies import DependenceProtocol


class Postgres(DependenceProtocol):

    def __init__(self):
        super().__init__()
        self.pg_user: str = self.env_var.get('PG_USER')
        self.pg_db: str = self.env_var.get('PG_DB')
        self.pg_host: str = self.env_var.get('PG_HOST')
        self.pg_pass: str = self.env_var.get('PG_PASS')
        self.conn: Optional[asyncpg.Connection] = None


    async def __connect(self) -> None:
        self.conn = await asyncpg.connect(
            user=self.pg_user,
            password=self.pg_pass,
            database=self.pg_db,
            host=self.pg_host,
        )

    async def execute(self, command: str, params: Any = None) -> Any:
        if not self.conn:
            await self.__connect()
        res = await self.conn.execute(command, params) if params else await self.conn.execute(command)
        return res

    async def fetch(self, command: str, params: Any = None) -> Any:
        if not self.conn:
            await self.__connect()
        res: list[asyncpg.Record] = await self.conn.fetch(command, params) if params else await self.conn.fetch(command)
        return res
