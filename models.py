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

class ArtNight(Base):
    __tablename__ = 'art_night'

    id = Column(Integer, primary_key = True)
    city = Column(String(50), nullable = False)
    title = Column(String(100), nullable = False)
    description = Column(String(1000), nullable = False)
    project_img = Column(String(200), nullable = False)
    date = Column(String(50), nullable = False)
    time = Column(String(50), nullable = False)
    cost = Column(String(50), nullable = False)
    location = Column(String(250), nullable = False)
    address = Column(String(100), nullable = False)
    upcoming_date_1 = Column(String(50), nullable = False)
    upcoming_date_2 = Column(String(50), nullable = False)
    upcoming_date_3 = Column(String(50), nullable = False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)


class BlogPost(Base):
    __tablename__ = 'blogPost'

    title = Column(String(100), nullable = False)
    subtitle = Column(String(500), nullable = True)
    id = Column(Integer, primary_key = True)
    authorName = Column(String(50), nullable = False)
    authorImg = Column(String(50), nullable = False)
    authorDescription = Column(String(200), nullable = False)
    mainImg = Column(String(50), nullable = False)
    date = Column(String(20), nullable = False)
    category = Column(String(50), nullable = False)
    img_1 = Column(String(50), nullable = False, default='')
    img_2 = Column(String(50), nullable = True)
    img_3 = Column(String(50), nullable = True)
    img_4 = Column(String(50), nullable = True)
    img_5 = Column(String(50), nullable = True)
    img_6 = Column(String(50), nullable = True)
    img_7 = Column(String(50), nullable = True)
    img_8 = Column(String(50), nullable = True)
    img_9 = Column(String(50), nullable = True)
    img_10 = Column(String(50), nullable = True)
    body_1 = Column(String(3000), nullable = False)
    body_2 = Column(String(3000), nullable = True)
    body_3 = Column(String(3000), nullable = True)
    body_4 = Column(String(3000), nullable = True)
    body_5 = Column(String(3000), nullable = True)
    body_6 = Column(String(3000), nullable = True)
    body_7 = Column(String(3000), nullable = True)
    body_8 = Column(String(3000), nullable = True)
    body_9 = Column(String(3000), nullable = True)
    body_10 = Column(String(3000), nullable = True)
    body_header_1 = Column(String(500), nullable = True)
    body_header_2 = Column(String(500), nullable = True)
    body_header_3 = Column(String(500), nullable = True)
    body_header_4 = Column(String(500), nullable = True)
    body_header_5 = Column(String(500), nullable = True)
    body_header_6 = Column(String(500), nullable = True)
    body_header_7 = Column(String(500), nullable = True)
    body_header_8 = Column(String(500), nullable = True)
    body_header_9 = Column(String(500), nullable = True)
    body_header_10 = Column(String(500), nullable = True)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        return {
            'title': self.title,
            'subtitle': self.subtitle,
            'id': self.id,
            'authorName': self.authorName,
            'authorImg' : self.authorImg,
            'authorDescription' : self.authorDescription,
            'mainImg': self.mainImg,
            'date': self.date,
            'category' : self.category,
            'img_1' : self.img_1,
            'body_header_1': self.body_header_1,
            'body_1': self.body_1,
            'img_2' : self.img_2,
            'body_header_2': self.body_header_2,
            'body_2': self.body_2,
            'img_3' : self.img_3,
            'body_header_3': self.body_header_3,
            'body_3': self.body_3,
            'img_4' : self.img_4,
            'body_header_4': self.body_header_4,
            'body_4': self.body_4,
            'img_5' : self.img_5,
            'body_header_5': self.body_header_5,
            'body_5': self.body_5,
            'img_6' : self.img_6,
            'body_header_6': self.body_header_6,
            'body_6': self.body_6,
            'img_7' : self.img_7,
            'body_header_7': self.body_header_7,
            'body_7': self.body_7,
            'img_8' : self.img_8,
            'body_header_8': self.body_header_8,
            'body_8': self.body_8,
            'img_9' : self.img_9,
            'body_header_9': self.body_header_9,
            'body_9': self.body_9,
            'img_10' : self.img_10,
            'body_header_10': self.body_header_10,
            'body_10': self.body_10
        }


#instance of create_engine
engine = create_engine('sqlite:///amyzanderdb.db')

Base.metadata.create_all(engine)
