"""
Defines the database tables. Each class corresponds to a table
There is a users table and a posts table

How it will be used:
from models import User, Post
--> next time you can just call db.query(User) or like User(....) to create a new entry

"""




from sqlalchemy import Boolean, Column, Integer, String
from database import Base 
# run the database.py script and import the Base that we've created

class User(Base):
    __tablename__ = 'users'

    # by setting index is true, you say this is going to be the term you use to fetch data from database
    # index = True --> ENABLES FAST LOOKUP FROM DB.
    id = Column(Integer, primary_key = True, index = True)

    # setting string(50) means it is a varchar with max size 50
    username = Column(String(50), unique=True)


class Post(Base):
    __tablename__ = 'posts' # set the table name
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(50))
    content = Column(String(100))
    user_id = Column(Integer)
