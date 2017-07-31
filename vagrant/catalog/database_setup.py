# Database Configuration file using SQLAlchemy
import os
import sys

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

### Table Class ####
Base = declarative_base()

### Each classe represent Table
### Each Column Represent field within the table

class Restaurant(Base):
    ### Restaurant Table #####
    __tablename__ = 'restaurant'

    ### Columns ####
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'id': self.id,
        }

class MenuItem(Base):
    #### Menue Table #####
    __tablename__ = 'menu_item'

    ### Columns ####
    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    description = Column(String(250))
    price = Column(String(8))
    course = Column(String(250))
    restaurant_id = Column(Integer, ForeignKey('restaurant.id'))
    restaurant = relationship(Restaurant)

# We added this serialize function to be able to send JSON objects in a
# serializable format
    @property
    def serialize(self):

        return {
            'name': self.name,
            'description': self.description,
            'id': self.id,
            'price': self.price,
            'course': self.course,
        }


########## Create the DB ################

engine = create_engine('sqlite:///restaurantmenu.db')

Base.metadata.create_all(engine)
