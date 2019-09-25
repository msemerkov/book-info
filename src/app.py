import multiprocessing

from aiorun import run
from sanic import Sanic

from src.books.router import group as books_group
from src.db_conn import SAConn

app = Sanic()

app.blueprint(books_group)


@app.listener('before_server_start')
async def init(_, loop):
    await SAConn.init_db_connect(loop)


@app.listener('after_server_stop')
async def shutdown(*_):
    await SAConn.close()


def main():
    app.run(
        host="0.0.0.0", port=8000,
        workers=multiprocessing.cpu_count(),
        debug=False, auto_reload=True
    )


if __name__ == "__main__":
    run(main())
