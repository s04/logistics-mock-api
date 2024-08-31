from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from ..models.database import get_db
from ..models.item import Item
from pydantic import BaseModel

router = APIRouter()


class ItemInput(BaseModel):
    name: str
    description: str = None
    price: float
    stock: int


class ItemOutput(ItemInput):
    id: int

    class Config:
        orm_mode = True


@router.options("/items")
async def options_items():
    return JSONResponse(
        status_code=200,
        headers={
            "Allow": "GET, POST, OPTIONS",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
            "Access-Control-Allow-Headers": "Authorization, Content-Type",
        },
    )


@router.get("/items", response_model=list[ItemOutput])
def list_items(limit: int = 20, offset: int = 0, db: Session = Depends(get_db)):
    items = db.query(Item).offset(offset).limit(limit).all()
    return items


@router.post("/items", response_model=ItemOutput, status_code=201)
def create_item(item: ItemInput, db: Session = Depends(get_db)):
    db_item = Item(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


@router.get("/items/{item_id}", response_model=ItemOutput)
def get_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(Item).filter(Item.id == item_id).first()
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@router.put("/items/{item_id}", response_model=ItemOutput)
def update_item(item_id: int, item: ItemInput, db: Session = Depends(get_db)):
    db_item = db.query(Item).filter(Item.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    for key, value in item.dict().items():
        setattr(db_item, key, value)
    db.commit()
    db.refresh(db_item)
    return db_item


@router.delete("/items/{item_id}", status_code=204)
def delete_item(item_id: int, db: Session = Depends(get_db)):
    db_item = db.query(Item).filter(Item.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(db_item)
    db.commit()
    return None
