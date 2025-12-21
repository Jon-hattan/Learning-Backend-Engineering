from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
from typing import Annotated
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session


app = FastAPI(root_path="/api/v1")

# Looks at all the classes that inherit from the models.Base
# Reads column definitions, creates the actual tables in the database if they dont already exist.
"""
models.Base.metadata.create_all(bind=engine)  ## ONLY FOR PROTOTYPING
IN PRODUCTION: this line is not used. it doesnt handle schema changes
This literally recreates the tables. 
It does this: Creates all database tables defined in my SQLAlchemy models if they do not already exist, but do not manage changes.
Prod databases require safe migrations
Need to do something called ALEMBIC MIGRATIONS
"""

"""ALEMBIC MIGRATIONS"""

# Create Pydantic Model for Post
class PostBase(BaseModel):
    title: str
    content: str
    user_id: int

class PostResponse(BaseModel):
    id: int
    title: str
    content: str
    user_id: int

    model_config = {
        "from_attributes": True
    }

class UserBase(BaseModel):
    username: str

class UserResponse(BaseModel):
    id: int
    username: str

    model_config = {
        "from_attributes": True
    }
    # this means that when validating this model, 
    # you are allowed to read values from an object’s attributes 
    # not just dictionaries

def get_db(): # RETURNS A SESSION OBJECT
    db = SessionLocal()
    try:   
    # YIELD: same as return, but it runs EXTRA CLEANUP after the function finishes
        yield db 
    finally:
        db.close()

# the code below only makes it such that you dont need to write Session = Depends(get_db) all the time
# NOT compulsory. it means everytime you want to write that you just write db_dependency
# db_dependency = Annotated(Session, Depends(get_db))




"""
In FastAPI function definition parameters:
- Anything marked as “Pydantic model” goes to the JSON handler.
- Anything marked as “Depends” goes to the dependency handler.
- Anything marked int/str goes to path/query parser.

JSON HANDLER:
- when your parameter type is a Pydantic model / dict or list (with body) / Body annotated types
- FastAPI automatically:
    - Reads the JSON
    - Validates it using the Pydantic model
    - Converts it into a Python object
    - Passes it into the function

DEPENDENCY HANDLER:
(i.e before you run this function, prepare something for me)
- Triggered when you annotate a parameter with Depends(...)
- only handles depends(..) parameters, background tasks, auth, database..
    - FastAPI sees Depends(get_db) and says: “This is NOT from JSON, I need to call the function get_db() to generate this value.”
    - Calls get_db()
    - Takes the db session it yields
    - Injects it into the function

QUERY PARSER:
- for simple types
- EG: 
    @app.get("/users/{user_id}")
    def get_user(user_id: int):
- FastAPI concludes that user_id must come from the path.”
    - The request:
    - GET /users/123
    - passes user_id = 123 into your function.

ORDER OF PARAMETERS IN THE FUNCTION:
1. Path parameters
2. Body parameters (Pydantic models)
3. Dependencies (with Defaults)
"""
@app.post("/users/", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
# parameters are: param_name: type hint. So db is of type Session, and has the value of the value returned by get_db
async def create_user(user: UserBase, db: Session = Depends(get_db)): # Session=Depends(get_db) means to get a db session, call function getdb
    db_user = models.User(**user.model_dump()) # convert the pydantic model to ORM model
    # .model_dump converst the json (pydantic format) to dict
    # ** is dictionary unpacking --> basically means it passes the key value pairs as arguments
    # models.User(...) basically makes an ORM object from the parameters of the json file
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
# when you return the db_user object, FastAPI matches it to the response model UserResponse
# FastAPI basically returns the json for you, by converting it for you

# if the return value is not compatible or has missing fields --> validation error


@app.get("/users/", status_code=status.HTTP_200_OK, response_model=list[UserResponse])
async def get_all_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users



"""
SQLALCHEMY COMMANDS

db.add(x: ORM object) --> add that entry into the table it belongs to (NOT COMMITTED YET)
db.commit() --> Writes all pending changes in the session to the actual database.
db.refresh(x: ORM object) --> refresh the db for that specific entry
db.query(y: ORM object TYPE).filter(y.attribute1 = "example") --> returns a QUERY OBJECT, not a list yet.
    - ^^^.all() --> returns the list 
    - ^^^.first() --> returns the first entry
    - ^^^.count() --> int
    - ^^^.one() --> raise error if not one
db.query(y: ORM  object TYPE).all() --> returns a list of all entries in that table
db.query(y: ORM object TYPE).first() --> returns the first entry
db.get(Model, primary_key) --> returns row with that primary key , returns none if not found
db.delete(x: ORM object) --> delete that entry
db.rollback() --> undo uncommitted changes

CHANGING INDIVIDUAL ENTRIES:
-> use x = db.get(Model, primary_key) to get the entry
-> x.attribute1 = something else
-> db.commit
-> db.refresh(x) to refresh that entry to return it
"""



# PRACTICE ENDPOINTS
@app.get("/users/{user_id}", response_model=UserBase)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.get(models.User, user_id)
    if user:
        return user # FastApi can strip out all the other fields automatically, to make it userbase form
    else:
        raise HTTPException(status_code=404, detail="id does not exist in database")

@app.delete("/users/{user_id}", response_model=UserResponse)
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.get(models.User, user_id)
    if user:
        db.delete(user)
        db.commit()
        return user
    else:
        raise HTTPException(status_code=404, detail="id does not exist in database")
    
@app.put("/users/{user_id}", response_model=UserBase)
async def update_username( user_id: int, user_update: UserBase, db: Session = Depends(get_db)):
    user = db.get(models.User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="id does not exist in database")
    user.username = user_update.username # ORM OBJECT IS A LIVE INSTANCE, YOU CHANGE IT MEANS CHANGING THE DATABASE IN THE TRANSACTION
    db.commit()
    db.refresh(user)
    return user





@app.post("/posts/", response_model=PostResponse)
async def create_post(user_post: PostBase, db: Session = Depends(get_db)):
    post = models.Post(**user_post.model_dump()) #create orm object
    user = db.get(models.User, post.user_id) # check if id exists
    if not user:
        raise HTTPException(status_code=404, detail="id does not exist in database")
    db.add(post)
    db.commit()
    db.refresh(post)
    return post

@app.get("/posts/",  response_model=list[PostResponse])
async def get_all_posts(db: Session = Depends(get_db)):
    all_posts = db.query(models.Post).all()
    if not all_posts:
        raise HTTPException(status_code=404, detail="no posts in database")
    else:
        return all_posts
    

"""
NEXT UP:
- DATABASE MIGRATIONS (ALEMBIC)
- USER AUTH
- ERROR HANDLING
- ENV VARIABLES (which we already kinda did)

"""


"""
ALEMBIC MIGRATIONS
in terminal, run "alembic init migrations" to create the necessary folders
Alembic migrations let your database schema change safely over time by recording
 each schema change (like adding a column or table) as a versioned, ordered, and 
 reversible step, so existing data is preserved and every environment can be upgraded 
 or rolled back in a controlled way instead of recreating tables.

"""



"""
****RUNNING AND TESTING****

FASTAPI itself doesnt run, need a ASGI Server
- Use Uvicorn
uvicorn main:app --reload
--> main is the filename
--> app is the FastAPI object
--> --reload param means it auto restarts on code changes.

ADD "docs" to the end of the url to access the Swagger UI, which makes it easy to test it.
http://127.0.0.1:8000/docs
"""