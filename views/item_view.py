# views/item_view.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from repositry.repositry_Item import create_item, get_item_postgres, update_post, \
    delete_pgres, up_partially, get_all_mongo, get_all_items_postgres, create_item_mongodb, update_mongodb, \
    delete_mongodb_item, get_item_mongo

from Serializers.item_serializers import ItemSerializer, AllItemsResponse
from models.item_models import Item, items_collection
from settings.Postgres_connections import get_db

router = APIRouter()


# Dependency to get PostgreSQL session


# Create item in PostgreSQL
@router.post("/items/")
def create_item_postgres(item: ItemSerializer, db: Session = Depends(get_db)):
    return create_item(item, db)


@router.get("/items/", response_model=AllItemsResponse)
def get_items(db: Session = Depends(get_db)):
    return get_all_items_postgres(db)


@router.get("/items/{item_id}/", response_model = ItemSerializer)
def get_item_by_id(item_id: int, db: Session = Depends(get_db)):
    return get_item_postgres(db, item_id)


@router.put("/items/{item_id}")
def update_item(item_id: int, item: ItemSerializer, db: Session = Depends(get_db)):
    return update_post(item_id, item, db)

@router.patch("/items/{item_id}")
def update_partially(item_id : int, item: ItemSerializer, db : Session= Depends(get_db)):
    return up_partially(item_id,item,db)

@router.delete("/items/{item_id}")
def delete_item(item_id : int, db: Session =Depends(get_db)):
    return delete_pgres(item_id, db)
# Create item in MongoDB (Optional)
@router.post("/mongo_items/")
def create_item_mongo(item: ItemSerializer):
    return create_item_mongodb(item)
@router.get("/mongo_items/")
def get_all_items_mongo():
    return get_all_mongo()
@router.get("/mongo_items/{item_id}")
def get_item_by_id(item_id):
    return get_item_mongo(item_id)
@router.put("/{item_id}")
def update_mongodb_item(item_id: str, item: ItemSerializer):
   return update_mongodb(item_id, item)

@router.delete("/{item_id}")
def delete_mongo_item(item_id: str):
    return delete_mongodb_item(item_id)