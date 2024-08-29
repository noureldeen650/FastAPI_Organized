from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
from sqlalchemy.orm import Session
from pymongo.mongo_client import MongoClient
from bson import ObjectId
import models
from database import engine, SessionLocal, items_collection
from models import PostgresItem


# PostgreSQL setup
models.Base.metadata.create_all(bind=engine)

# MongoDB setup
uri = "mongodb+srv://admin:swarco@cluster0.gk11g.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri)
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

app = FastAPI()

class ItemModel(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Depends(get_db)

# PostgreSQL Endpoints
@app.post("/items/", response_model=ItemModel)
def add_item(item: ItemModel, db: Session = db_dependency):
    db_item = PostgresItem(name=item.name, description=item.description, price=item.price)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@app.get("/items/", response_model=List[ItemModel])
def get_items(db: Session = db_dependency):
    return db.query(PostgresItem).all()

@app.get("/items/{item_id}", response_model=ItemModel)
def get_item(item_id: int, db: Session = db_dependency):
    result = db.query(PostgresItem).filter(PostgresItem.id == item_id).first()
    if not result:
        raise HTTPException(status_code=404, detail="Item not found")
    return result

@app.put("/items/{item_id}", response_model=ItemModel)
def update_item(item_id: int, item: ItemModel, db: Session = db_dependency):
    db_item = db.query(PostgresItem).filter(PostgresItem.id == item_id).first()
    if db_item:
        db_item.name = item.name
        db_item.description = item.description
        db_item.price = item.price
        db.commit()
        db.refresh(db_item)
        return db_item
    raise HTTPException(status_code=404, detail="Item not found")

@app.patch("/items/{item_id}", response_model=ItemModel)
def update_item_partially(item_id: int, item: ItemModel, db: Session = db_dependency):
    db_item = db.query(PostgresItem).filter(PostgresItem.id == item_id).first()
    if db_item:
        update_data = item.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_item, key, value)
        db.commit()
        db.refresh(db_item)
        return db_item
    raise HTTPException(status_code=404, detail="Item not found")

@app.delete("/items/{item_id}", response_model=dict)
def delete_item(item_id: int, db: Session = db_dependency):
    db_item = db.query(PostgresItem).filter(PostgresItem.id == item_id).first()
    if db_item:
        db.delete(db_item)
        db.commit()
        return {"detail": "Item deleted successfully"}
    raise HTTPException(status_code=404, detail="Item not found")

# MongoDB Endpoints

@app.post("/mongodb/items/", response_model=dict)
def add_mongodb_item(item: ItemModel):
    item_data = item.dict(exclude_unset=True)
    result = items_collection.insert_one(item_data)
    created_item = items_collection.find_one({"_id": result.inserted_id})
    created_item["_id"] = str(created_item["_id"])
    return created_item

@app.get("/mongodb/items/", response_model=List[dict])
def get_mongodb_items():
    items = list(items_collection.find())
    for item in items:
        item["_id"] = str(item["_id"])
    return items

@app.get("/mongodb/items/{item_id}", response_model=dict)
def get_mongodb_item(item_id: str):
    item = items_collection.find_one({"_id": ObjectId(item_id)})  # Convert string ID to ObjectId
    if item:
        item["_id"] = str(item["_id"])
        return item
    raise HTTPException(status_code=404, detail="Item not found")

@app.put("/{item_id}")
def update_mongodb_item(item_id: str, item: ItemModel):
    result = items_collection.find_one_and_update({"_id": ObjectId(item_id)}, {"$set": dict(item)})
    if not result:
        raise HTTPException(status_code=404, detail="Item not found")
    return result


@app.patch("/mongodb/items/{item_id}", response_model=dict)
def update_partially_mongodb_item(item_id: str, item: ItemModel):
    item_data = item.dict(exclude_unset=True)
    result = items_collection.update_one({"_id": ObjectId(item_id)}, {"$set": item_data})  # Convert string ID to ObjectId
    if result.modified_count > 0:
        updated_item = items_collection.find_one({"_id": ObjectId(item_id)})  # Convert string ID to ObjectId
        updated_item["_id"] = str(updated_item["_id"])  # Convert ObjectId to string
        return updated_item
    raise HTTPException(status_code=404, detail="Item not found")

@app.delete("/{item_id}")
def delete_mongodb_item(item_id: str):
    result = items_collection.find_one_and_delete({"_id": ObjectId(item_id)})  # Convert string ID to ObjectId
    if result:
        return {"detail": "Item deleted successfully"}
    raise HTTPException(status_code=404, detail="Item not found")





