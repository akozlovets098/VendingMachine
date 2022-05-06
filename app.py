from models import Category
from fastapi import FastAPI, Query
from database import db
from datetime import date

app = FastAPI()


@app.get('/')
def hello():
    return f'Welcome to the main page'


@app.get('/list')
def leftovers_list():
    for item in db:
        yield f'{item.name} costs {item.price} UAH. Quantity available: {item.quantity}.'


@app.post('/list')
def add_category(category: Category):
    new_category = Category(**category.dict())
    for item in db:
        if item.name == new_category.name:
            return 'This category already exists'
    db.append(new_category)
    return f'"{new_category.name}" category was successfully added.'


@app.post('/list/{category}')
def purchase(category, date_of_purchase: date = date.today()):
    for item in db:
        if item.name == category:
            if item.quantity > 0:
                item.quantity -= 1
                return f'You purchased {item.name} for {item.price}. Date: {date_of_purchase}'
            else:
                return f'There left none of {item.name}'
    return 'There is no such category'


@app.put('/list/{category}')
def add_items(quantity: int, category: str):
    for item in db:
        if item.name == category:
            item.quantity += quantity
            return f'{item.name} quantity was successfully increased by {quantity}'


@app.delete('/list')
def delete_empty_categories():
    indices_to_delete = []
    for item in db:
        if item.quantity <= 0:
            indices_to_delete.append(db.index(item))
    if len(indices_to_delete) == 0:
        return 'There are no empty categories'
    for i in indices_to_delete[::-1]:
        db.remove(db[i])
    return f'Empty categories deleted: {len(indices_to_delete)}'