import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

#instance of declarative_base
Base = declarative_base()

#declaring a class
class Category(Base):
    #naming the table
    __tablename__ = 'category'
    #creating mappers
    name = Column(String(20), nullable = False)
    #declaring the primary key
    id = Column(Integer, primary_key = True)

#declaring a class
class Item(Base):
    #naming the table
    __tablename__ = 'item'
    #creating mappers
    name = Column(String(50), nullable = False)
    id = Column(Integer, primary_key = True)
    description = Column(String(250))
    price = Column(String(8))
    #declaring the foreign key
    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship(Category)

#instance of create_engine
engine = create_engine('sqlite:///amyzandershop.db')

Base.metadata.create_all(engine)
