import sqlalchemy
import json
from sqlalchemy.orm import sessionmaker
from models import create_tables, Publisher, Book, Stock, Shop, Sale

DSN = "postgresql://postgres:Pderfhm86@localhost:5432/ORM_db2"
engine = sqlalchemy.create_engine(DSN)
create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()

with open('tests_data.json', 'r') as fd:
    data = json.load(fd)

for record in data:
    model = {
        'publisher': Publisher,
        'shop': Shop,
        'book': Book,
        'stock': Stock,
        'sale': Sale,
    }[record.get('model')]
    session.add(model(id=record.get('pk'), **record.get('fields')))

request = input('Input Publisher.name or Publisher.id: ')
query = session.query(Book.title, Shop.name, Sale.price, Sale.date_sale).join(Publisher).join(Stock).join(Shop).join(Sale)
if request.isdigit():
    query = query.filter(Publisher.id == request).all()
else:
    query = query.filter(Publisher.name == request).all()

for title, name, price, date_sale in query:
    print(f"{title:<40} | {name:<10} | {price:<8} | {date_sale}")

session.commit()
session.close()

