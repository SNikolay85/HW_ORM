import json
import os
import sqlalchemy as sq
from sqlalchemy.orm import sessionmaker
from models import create_tables, Publisher, Book, Shop, Stock, Sale

def display(lst):
    size = [40, 10, 10, 30]
    lst.insert(0, ('Название книги', 'Магазин', 'Цена', 'Дата продажи'))
    lst.insert(1, ('-' * size[0], '-' * size[1], '-' * size[2], '-' * size[3]))
    for cl in lst:
        for i in range(len(cl)):
            text = str(cl[i])
            print(f'| {text.center(size[i])}', end=' ')
        print()

def load_db(data):
    for str in data:
        if str['model'] == 'publisher':
            pub = Publisher(id_publisher=str['pk'], name=str['fields']['name'])
            session.add(pub)
            session.commit()
        elif str['model'] == 'book':
            book = Book(id_book=str['pk'], title=str['fields']['title'], id_publisher=str['fields']['publisher'])
            session.add(book)
            session.commit()
        elif str['model'] == 'shop':
            shop = Shop(id_shop=str['pk'], name=str['fields']['name'])
            session.add(shop)
            session.commit()
        elif str['model'] == 'stock':
            stock = Stock(id_stock=str['pk'], id_book=str['fields']['book'], id_shop=str['fields']['shop'], count=str['fields']['count'])
            session.add(stock)
            session.commit()
        elif str['model'] == 'sale':
            sale = Sale(id_sale=str['pk'], price=float(str['fields']['price']), date_sale=str['fields']['date_sale'], id_stock=str['fields']['stock'], count=str['fields']['count'])
            session.add(sale)
            session.commit()
    return print('Данные считаны и загружены в БД')

with open('D:\Python\pas.txt', encoding='utf-8') as file:
    pas = file.read()

DSN = f'postgresql://postgres:{pas}@localhost:5432/magazine_of_publisher'
engine = sq.create_engine(DSN)

create_tables(engine)

Session = sessionmaker(bind=engine)

current = os.getcwd()
file_name = 'tests_data.json'
full_path = os.path.join(current, file_name)

session = Session()

with open(full_path, 'r', encoding='utf-8') as file:
    data = json.load(file)

load_db(data)
print()
question = input('Введи издателя: ')
print()
q = session.query(Publisher, Book.title, Shop.name, Sale.date_sale, Sale.price).join(Book).join(Stock).join(Shop).join(Sale).filter(Publisher.name == f'{question}').all()

lst = []
for s in q:
    lst.append([s.title, s.name, float(s.price), s.date_sale])

display(lst)
session.close()
