from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = '<replace with a secret key>'
# toolbar = DebugToolbarExtension(app)

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# Fake Restaurants
# restaurant = {'name': 'The CRUDdy Crab', 'id': '1'}

# restaurants = [{'name': 'The CRUDdy Crab', 'id': '1'}, {'name':'Blue Burgers', 'id':'2'},{'name':'Taco Hut', 'id':'3'}]


# Fake Menu Items
# items = [ {'name':'Cheese Pizza', 'description':'made with fresh cheese', 'price':'$5.99','course' :'Entree', 'id':'1'}, {'name':'Chocolate Cake','description':'made with Dutch Chocolate', 'price':'$3.99', 'course':'Dessert','id':'2'},{'name':'Caesar Salad', 'description':'with fresh organic vegetables','price':'$5.99', 'course':'Entree','id':'3'},{'name':'Iced Tea', 'description':'with lemon','price':'$.99', 'course':'Beverage','id':'4'},{'name':'Spinach Dip', 'description':'creamy dip with fresh spinach','price':'$1.99', 'course':'Appetizer','id':'5'} ]
# item =  {'name':'Cheese Pizza','description':'made with fresh cheese','price':'$5.99','course' :'Entree'}


@app.route('/')
@app.route('/restaurants')
def showRestaurants():
    restaurants = session.query(Restaurant).all()
    return render_template('restaurants.html', restaurants=restaurants)


@app.route('/restaurants/new', methods=['GET', 'POST'])
def newRestaurant():
    if request.method == 'POST':
        newRestaurant = Restaurant(name=request.form['name'])
        session.add(newRestaurant)
        session.commit()
        # flash("New restaurant created!")
        return redirect(url_for('showRestaurants'))
    else:
        return render_template('newrestaurant.html')


@app.route('/restaurants/<int:restaurant_id>/edit', methods=['GET', 'POST'])
def editRestaurant(restaurant_id):
    editedRestaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedRestaurant.name = request.form['name']
            session.add(editedRestaurant)
            session.commit()
            # flash("New restaurant created!")
            return redirect(url_for('showRestaurants'))
    else:
        return render_template('editrestaurant.html', restaurant=editrestaurant)


@app.route('/restaurants/<int:restaurant_id>/delete', methods=['GET', 'POST'])
def deleteRestaurant(restaurant_id):
    deletedRestaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        session.delete(deletedRestaurant)
        session.commit()
        # flash("New restaurant created!")
        return redirect(url_for('showRestaurants'))
    else:
        return render_template('deleterestaurant.html', restaurant=deleteRestaurant)


@app.route('/restaurants/<int:restaurant_id>/')
@app.route('/restaurants/<int:restaurant_id>/menu')
def restaurantMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    itemsAppetizer = session.query(MenuItem).filter_by(restaurant_id=restaurant_id).filter_by(course='Appetizer')
    itemsBeverage = session.query(MenuItem).filter_by(restaurant_id=restaurant_id).filter_by(course='Beverage')
    itemsEntree = session.query(MenuItem).filter_by(restaurant_id=restaurant_id).filter_by(course='Entree')
    itemsDessert = session.query(MenuItem).filter_by(restaurant_id=restaurant_id).filter_by(course='Dessert')
    return render_template(
        'menu.html', restaurant=restaurant, itemsAppetizer=itemsAppetizer, itemsBeverage=itemsBeverage,
        itemsDessert=itemsDessert, itemsEntree=itemsEntree, restaurant_id=restaurant_id)


@app.route('/restaurants/<int:restaurant_id>/new', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()

    if request.method == 'POST':
        newItem = MenuItem
        if request.form['name']:
            print "name - " + request.form['name']
            newItem.name = request.form['name']
        if request.form['description']:
            print "description -" + request.form['description']
            newItem.description = request.form['description']
        if request.form['price']:
            print "price - " + request.form['price']
            newItem.price = request.form['price']
        if request.form['course']:
            print "course - " + request.form['course']
            newItem.course = request.form['course']
        print "restaurant_id - " + str(restaurant_id)
        newItem.restaurant_id = restaurant_id
        print "restaurant = " + restaurant.name
        newItem.restaurant = restaurant

            #print newItem
        session.add(newItem)
        session.commit()
        # flash("new menu item created!")
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant.id))
    else:
        # return render_template('newmenuitem.html', restaurant_id=restaurant_id, restaurant=restaurant)
        return render_template('newmenuitem.html', restaurant=restaurant)


@app.route('/restaurants/<int:restaurant_id>/<int:item_id>/edit', methods=['GET', 'POST'])
def editMenuItem(restaurant_id, item_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    editedItem = session.query(MenuItem).filter_by(id=item_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        if request.form['description']:
            # print "description -" + request.form['description']
            editedItem.description = request.form['description']
        if request.form['price']:
            # print "price - " + request.form['price']
            editedItem.price = request.form['price']
        if request.form['course']:
            #print "course - " + request.form['course']
            editedItem.course = request.form['course']
        #print "restaurant_id - " + str(restaurant_id)
        #newItem.restaurant_id = restaurant_id
        #print "restaurant = " + restaurant.name
        session.add(editedItem)
        #flash("Menu Item has been edited")
        session.commit()
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant.id))
    else:
        return render_template(
            'editmenuitem.html', item=editedItem, restaurant=restaurant)



@app.route('/restaurants/<int:restaurant_id>/<int:item_id>/delete', methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, item_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    itemToDelete = session.query(MenuItem).filter_by(id=item_id).one()
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        #flash("Menu Item has been deleted")
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant.id))
    else:
        return render_template('deletemenuitem.html', item=itemToDelete, restaurant=restaurant)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
