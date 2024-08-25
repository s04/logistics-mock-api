from fastapi import FastAPI
from .routers import items, orders
from .models.database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Items and Orders API", version="1.0.0")

app.include_router(items.router, tags=["items"])
app.include_router(orders.router, tags=["orders"])


@app.get("/")
async def root():
    return {"message": "Welcome to the Items and Orders API"}


# Seed the database with some dummy data
from .models.database import SessionLocal
from .models.item import Item
from .models.order import Order, OrderItem, OrderStatus


def seed_database():
    db = SessionLocal()

    # Seed items
    items = [
        Item(name="Item 1", description="Description 1", price=10.99, stock=100),
        Item(name="Item 2", description="Description 2", price=20.99, stock=50),
        Item(name="Item 3", description="Description 3", price=15.99, stock=75),
    ]
    db.add_all(items)
    db.commit()

    # Seed orders
    order = Order(
        customer_id="customer1", total_amount=47.97, status=OrderStatus.pending
    )
    order_items = [
        OrderItem(item_id=1, quantity=2),
        OrderItem(item_id=2, quantity=1),
    ]
    order.items.extend(order_items)
    db.add(order)
    db.commit()

    db.close()


# Call the seed_database function when the app starts
@app.on_event("startup")
async def startup_event():
    seed_database()
