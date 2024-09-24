# models/item_model.py

from sqlalchemy import Column, Integer, String,Float
from sqlalchemy.orm import declarative_base



# PostgreSQL Setup
Base = declarative_base()

class Item(Base):
    __tablename__ = 'items'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    price = Column(Float)
# MongoDB (Optional: If you are using MongoDB)

from pymongo import MongoClient
client = MongoClient("mongodb+srv://admin:swarco@cluster0.gk11g.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client.Cluster0
items_collection = db["items_collection"]