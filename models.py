import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

#instance of declarative_base
Base = declarative_base()

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable = False)
    password = Column(String(100), nullable = False)

class Category(Base):
    __tablename__ = 'category'

    name = Column(String(20), nullable = False)
    id = Column(Integer, primary_key = True)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        return {
            'name': self.name,
            'id': self.id
        }


class Item(Base):
    __tablename__ = 'item'

    name = Column(String(50), nullable = False)
    id = Column(Integer, primary_key = True)
    description = Column(String(250))
    price = Column(String(8))
    img = Column(String(50))
    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship(Category)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        return {
            'name': self.name,
            'id': self.id,
            'description': self.description,
            'price': self.price,
            'img': self.img
        }


class BlogPost(Base):
    __tablename__ = 'blog_post'

    title = Column(String(100), nullable = False)
    subtitle = Column(String(100))
    id = Column(Integer, primary_key = True)
    author = Column(Integer, nullable = False)
    img = Column(String(50), nullable = False)
    date = Column(String(20), nullable = False)
    body_1 = Column(String(3000), nullable = False)
    body_2 = Column(String(3000))
    body_3 = Column(String(3000))
    body_4 = Column(String(3000))
    body_5 = Column(String(3000))
    body_header_1 = Column(String(100))
    body_header_2 = Column(String(100))
    body_header_3 = Column(String(100))
    body_header_4 = Column(String(100))
    body_header_5 = Column(String(100))
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        return {
            'title': self.title,
            'subtitle': self.subtitle,
            'id': self.id,
            'author': self.title,
            'img': self.img,
            'date': self.date,
            'body_header_1': self.body_header_1,
            'body_1': self.body_1,
            'body_header_2': self.body_header_2,
            'body_2': self.body_2,
            'body_header_3': self.body_header_3,
            'body_3': self.body_3,
            'body_header_4': self.body_header_4,
            'body_4': self.body_4,
            'body_header_5': self.body_header_5,
            'body_5': self.body_5
        }


#instance of create_engine
engine = create_engine('sqlite:///amyzanderdb.db')

Base.metadata.create_all(engine)
