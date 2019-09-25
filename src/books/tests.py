from sanic.testing import SanicTestClient

from src.app import app


def test_books_list():
    request, response = SanicTestClient(app).get('/books')
    assert response.status == 200


def test_books_create():
    data = {
        "name": "new book",
        "author": "new book author",
        "rating": 3,
        "date_reading": "2019-03-03"
    }
    request, response = SanicTestClient(app).post('/books', data=data)
    assert response.status == 201


def test_book_not_found():
    request, response = SanicTestClient(app).get('/books/999')
    assert response.status == 404


def test_book_get():
    request, response = SanicTestClient(app).get('/books/2')
    assert response.status == 200


def test_books_update():
    data = {
        "name": "new book edit",
        "author": "new book author edit",
        "rating": 4,
        "date_reading": "2019-03-02"
    }
    request, response = SanicTestClient(app).put('/books/2', data=data)
    assert response.status == 200


def test_books_delete():
    request, response = SanicTestClient(app).delete('/books/2')
    assert response.status == 204
