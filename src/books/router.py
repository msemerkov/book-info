from sanic import Blueprint

from src.books.views import BookView, BooksView

books_bp = Blueprint('books')
books_bp.add_route(BooksView.as_view(), '/')
books_bp.add_route(BookView.as_view(), '/<id_arg:int>')

group = Blueprint.group(books_bp, url_prefix='/books')
