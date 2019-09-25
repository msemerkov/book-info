from sqlalchemy import Table, Column, Integer, String, MetaData, Date as AlchemyDate

metadata = MetaData()


class Date(AlchemyDate):
    def literal_processor(self, dialect):
        def process(value):
            return "'%s'" % value.strftime('%Y-%m-%d')
        return process


books = Table(
    'books', metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String),
    Column('author', String),
    Column('rating', Integer),
    Column('date_reading', Date),
)
