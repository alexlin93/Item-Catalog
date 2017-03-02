from flask import Flask, render_template
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Item

app = Flask(__name__)


# Connect to Database and create database session
engine = create_engine('sqlite:///itemcatalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# Home Page - Show all items by category
@app.route('/')
@app.route('/catalog/')
def showCategories():
    category = session.query(Category).order_by(asc(Category.name))
    items = session.query(Item).order_by(asc(Item.name))
    return render_template('catalog.html', category=category, items=items)


# Show a list of items under a category as a sidebar
@app.route('/catalog/<int:category_id>/')
def showItems(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    items = session.query(Item).filter_by(category_id=category_id).all()
    return render_template('catalog.html', items=items, category=category)


# Description Page - Show a description of the selected item
@app.route('/catalog/<int:category_id>/description/')
def showItemDescription(item_id, item_des):
    item = session.query(Category).filter_by(id=item_id).one()
    description = session.query(Item).filter_by(description=item_des).one()
    return render_template('item_description.html',
                           description=description, item=item)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
