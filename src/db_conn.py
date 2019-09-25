import json

import trafaret
from asyncpg.pool import create_pool
from sqlalchemy.dialects.postgresql.psycopg2 import PGDialect_psycopg2
from trafaret_config import read_and_validate

TRAFARET = trafaret.Dict({
    'postgres': trafaret.Dict({
        'host': trafaret.String(),
        'port': trafaret.Int(),
        'user': trafaret.String(),
        'password': trafaret.String(),
        'database': trafaret.String(),
    })
})


class SAConn:
    _pool = None

    _dialect = PGDialect_psycopg2(
        json_serializer=json.dumps,
        json_deserializer=lambda x: x,
        implicit_returning=True,
        supports_native_enum=True,
        supports_smallserial=True,
        supports_sane_multi_rowcount=True,
    )

    @classmethod
    async def init_db_connect(cls, loop):
        config = read_and_validate('configs/db.yaml', TRAFARET)
        cls._pool = await create_pool(loop=loop, **config['postgres'])

    @classmethod
    def compile_query(cls, query):
        return str(query.compile(dialect=cls._dialect, compile_kwargs={"literal_binds": True}))

    @classmethod
    async def execute(cls, query):
        async with cls._pool.acquire() as connection:
            async with connection.transaction():
                return await connection.execute(cls.compile_query(query))

    @classmethod
    async def prepare(cls, query):
        async with cls._pool.acquire() as connection:
            async with connection.transaction():
                stmt = await connection.prepare(cls.compile_query(query))
                async for record in stmt.cursor():
                    yield record

    @classmethod
    async def fetchrow(cls, query):
        async with cls._pool.acquire() as connection:
            async with connection.transaction():
                return await connection.fetchrow(cls.compile_query(query))

    @classmethod
    async def close(cls):
        await cls._pool.close()
