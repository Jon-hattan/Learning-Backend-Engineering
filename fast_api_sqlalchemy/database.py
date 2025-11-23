"""
All the application strings - to connect to SQL
Configures the database
Models inherit from the Base

This script is never actually called directly.
from .database import Base --> for eg.
at model import time, the script is executed
"""

from sqlalchemy import create_engine #to create the engine to communicate
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base 
from dotenv import load_dotenv
import os
load_dotenv()

URL_DATABASE = os.getenv("DATABASE_URL")

# engine is like the connection manager to the database
engine = create_engine(URL_DATABASE) # like the gateway for ORM sessions

# Session is a temporary database connection that makes the queries and changes
# similar to sqlite3.connect but it is more high level and has more functions
# set autocommit to false since you dont want to automatically commit after every query
# set autoflush to false, flush means push ORM changes to db before querying.

"""FLUSH"""
# Writes queries to DB, but it is contained within the transation (session)
# other users cannot see the changes yet, can be rolledback
# Feature is only avail in ORMs, not in sqlite

"""COMMIT"""
# Commits changes to database, other users can see

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a base class that all ORM models inherit from
# TELLS SQLALCHEMY WHICH CLASSES REPRESENT DATABASE TABLES, so its easy to store tables/column definitions
Base = declarative_base() 

