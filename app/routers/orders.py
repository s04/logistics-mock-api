from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..models.database import get_db
from ..models.order import Order, OrderItem, OrderStatus
from ..models.item import Item
from pydantic import BaseModel
from typing import List

router = APIRouter()


class OrderItemInput(BaseModel):
    item_id: int
    quantity: int


class OrderInput(BaseModel):
    customer_id: str
    items: List[OrderItemInput]


class OrderItemOutput(OrderItemInput):
    id: int

    class Config:
        orm_mode = True


class OrderOutput(BaseModel):
    id: int
    customer_id: str
    items: List[OrderItemOutput]
    total_amount: float
    status: OrderStatus
    created_at: str

    class Config:
        orm_mode = True


class OrderUpdate(BaseModel):
    status: OrderStatus


@router.get("/orders", response_model=List[OrderOutput])
def list_orders(limit: int = 20, offset: int = 0, db: Session = Depends(get_db)):
    orders = db.query(Order).offset(offset).limit(limit).all()
    return orders


@router.post("/orders", response_model=OrderOutput, status_code=201)
def create_order(order: OrderInput, db: Session = Depends(get_db)):
    db_order = Order(customer_id=order.customer_id, status=OrderStatus.pending)
    total_amount = 0
    for item in order.items:
        db_item = db.query(Item).filter(Item.id == item.item_id).first()
        if db_item is None:
            raise HTTPException(
                status_code=404, detail=f"Item {item.item_id} not found"
            )
        if db_item.stock < item.quantity:
            raise HTTPException(
                status_code=400, detail=f"Not enough stock for item {item.item_id}"
            )
        db_item.stock -= item.quantity
        total_amount += db_item.price * item.quantity
        db_order_item = OrderItem(item_id=item.item_id, quantity=item.quantity)
        db_order.items.append(db_order_item)
    db_order.total_amount = total_amount
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order


@router.get("/orders/{order_id}", response_model=OrderOutput)
def get_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@router.put("/orders/{order_id}", response_model=OrderOutput)
def update_order(
    order_id: int, order_update: OrderUpdate, db: Session = Depends(get_db)
):
    db_order = db.query(Order).filter(Order.id == order_id).first()
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    db_order.status = order_update.status
    db.commit()
    db.refresh(db_order)
    return db_order


@router.delete("/orders/{order_id}", status_code=204)
def delete_order(order_id: int, db: Session = Depends(get_db)):
    db_order = db.query(Order).filter(Order.id == order_id).first()
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    db.delete(db_order)
    db.commit()
    return None
