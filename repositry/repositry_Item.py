# repositories/item_repository.py
from fastapi import HTTPException
from fastapi.params import Depends

from Serializers.item_serializers import ItemSerializer
from models.item_models import Item, items_collection
from sqlalchemy.orm import Session

from settings.Postgres_connections import get_db
# args and kwargs

# PostgreSQL Repository
def create_item(item :ItemSerializer, db: Session ):
    db_item = Item(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def get_item_postgres(db: Session, item_id: int):
    item=  db.query(Item).filter(Item.id == item_id).first()
    return  item

def get_all_items_postgres(db: Session):
    items = db.query(Item).all()
    result = {"Items": items}
    return result


def update_post(item_id: int, item: ItemSerializer, db: Session):
    old = (db.query(Item).filter(Item.id == item_id).first())
    if old:
        old.name = item.name
        old.description = item.description
        old.price = item.price
        db.commit()
        db.refresh(old)
        return old
    raise HTTPException(status_code=404, detail="Item not found")

def up_partially(item_id : int,item: ItemSerializer, db: Session):
    db_item = db.query(Item).filter(Item.id == item_id).first()
    if db_item:
        update_data = item.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_item, key, value)
        db.commit()
        db.refresh(db_item)
        return db_item
    raise HTTPException(status_code=404, detail="Item not found")
def delete_pgres(item_id :int, db : Session):
    db_item = db.query(Item).filter(Item.id == item_id).first()
    if db_item:
        db.delete(db_item)
        db.commit()
        return "item deleted successfully"
    raise HTTPException(status_code=404, detail="Item not found")
# MongoDB Repository (Optional)
def create_item_mongodb(item: ItemSerializer):
    result = items_collection.insert_one(item)
    return result.inserted_id

def get_item_mongo(item_id):
    return items_collection.find_one({"_id": item_id})

def get_all_mongo():
    items = list(items_collection.find())
    for item in items:
        item["_id"] = str(item["_id"])
    return items
def update_mongodb(item_id: str, item: ItemSerializer):
    result = items_collection.find_one_and_update({"_id": Item(item_id)}, {"$set": dict(item)})
    if not result:
        raise HTTPException(status_code=404, detail="Item not found")
    return result

def delete_mongodb_item(item_id: str):
    result = items_collection.find_one_and_delete({"_id": Item(item_id)})  # Convert string ID to ObjectId
    if result:
        return {"detail": "Item deleted successfully"}
    raise HTTPException(status_code=404, detail="Item not found")