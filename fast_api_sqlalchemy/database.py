"""
All the application strings - to connect to SQL
"""

from sqlalchemy import create_engine #to create the engine to communicate
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base 
from dotenv import load_dotenv
import os
load_dotenv()

URL_DATABASE = os.getenv("DATABASE_URL")

#
engine = create_engine(URL_DATABASE)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

