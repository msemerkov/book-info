import trafaret as t
from datetime import datetime, date

DATE_FORMAT = '%Y-%m-%d'


class Date(t.Trafaret):
    def check_and_return(self, value):
        if not isinstance(value, date):
            self._failure("value is not a data", value=value)
        return value.strftime(DATE_FORMAT)


BOOK_TRAFARET = t.Dict({
    t.Key('id', optional=True): t.Int(),
    'name': t.String(),
    'author': t.String(),
    'rating': t.Int(),
    'date_reading': t.Or(
        t.String() >> (lambda value: datetime.strptime(value, DATE_FORMAT)),
        Date()
    ),
})

BOOKS_TRAFARET = t.List(BOOK_TRAFARET)
