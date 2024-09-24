# main.py

from fastapi import FastAPI
from views.item_view import router as item_router

app = FastAPI()

# Include the item routes
app.include_router(item_router)
