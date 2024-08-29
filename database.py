from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# PostgreSQL setup
URL_DATABASE = 'postgresql://postgres:swarco@localhost:5432/postgres'
engine = create_engine(URL_DATABASE)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# MongoDB setup
from pymongo import MongoClient
client = MongoClient("mongodb+srv://admin:swarco@cluster0.gk11g.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client.Cluster0
items_collection = db["items_collection"]
