import json

from sanic.response import json as json_response, HTTPResponse
from sanic.views import HTTPMethodView
from sqlalchemy.sql import select

from src.books.serializers import BOOK_TRAFARET
from src.books.tables import books
from src.db_conn import SAConn


class BooksView(HTTPMethodView):
    async def get(self, request, *args, **kwargs):
        query = select([books])
        data = []
        async for record in SAConn.prepare(query):
            data.append(BOOK_TRAFARET.check(dict(record)))
        return json_response(data)

    async def post(self, request, *args, **kwargs):
        data = BOOK_TRAFARET.check(json.loads(request.body))
        query = books.insert().values(data)
        await SAConn.execute(query)
        return HTTPResponse(status=201)


class BookView(HTTPMethodView):
    async def dispatch_request(self, request, *args, **kwargs):
        query = select([books]).where(books.c.id == kwargs['id_arg'])
        self.book = await SAConn.fetchrow(query)
        if not self.book:
            return HTTPResponse(status=404)
        return await super().dispatch_request(request, *args, **kwargs)

    async def get(self, request, *args, **kwargs):
        return json_response(dict(self.book))

    async def put(self, request, *args, **kwargs):
        data = BOOK_TRAFARET.check(json.loads(request.body))
        query = books.update().values(**data)
        await SAConn.execute(query)
        return HTTPResponse(status=200)

    async def delete(self, request, *args, **kwargs):
        query = books.delete()
        await SAConn.execute(query)
        return HTTPResponse(status=204)
