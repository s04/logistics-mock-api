from fastapi import FastAPI
from .routers import items, orders
from .models.database import engine, Base
import random
from datetime import datetime, timedelta
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Items and Orders API", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


class HSTSMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        response.headers["Strict-Transport-Security"] = (
            "max-age=31536000; includeSubDomains; preload"
        )
        return response


app.add_middleware(HSTSMiddleware)


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

    categories = {
        "Electronics": [
            ("Smartphone", 99.99, 1299.99),
            ("Laptop", 99.99, 1299.99),
            ("Tablet", 99.99, 1299.99),
            ("Headphones", 99.99, 1299.99),
            ("Smartwatch", 99.99, 1299.99),
            ("Camera", 99.99, 1299.99),
            ("Speaker", 99.99, 1299.99),
        ],
        "Home & Kitchen": [
            ("Coffee Maker", 29.99, 199.99),
            ("Blender", 29.99, 199.99),
            ("Toaster", 29.99, 199.99),
            ("Microwave", 29.99, 199.99),
            ("Air Fryer", 29.99, 199.99),
            ("Vacuum Cleaner", 29.99, 199.99),
        ],
        "Books": [
            ("Fiction Book", 9.99, 29.99),
            ("Non-fiction Book", 9.99, 29.99),
            ("Mystery Book", 9.99, 29.99),
            ("Sci-Fi Book", 9.99, 29.99),
            ("Biography Book", 9.99, 29.99),
            ("Self-help Book", 9.99, 29.99),
        ],
        "Clothing": [
            ("T-shirt", 19.99, 89.99),
            ("Jeans", 19.99, 89.99),
            ("Dress", 19.99, 89.99),
            ("Jacket", 19.99, 89.99),
            ("Sweater", 19.99, 89.99),
            ("Shoes", 19.99, 89.99),
        ],
        "Sports & Outdoors": [
            ("Running Shoes", 39.99, 399.99),
            ("Yoga Mat", 39.99, 399.99),
            ("Dumbbell Set", 39.99, 399.99),
            ("Camping Tent", 39.99, 399.99),
            ("Bicycle", 39.99, 399.99),
        ],
    }

    items = [
        Item(
            name=f"{name} {i}",
            description=(
                f"High-quality {name.lower()} with advanced features"
                if category == "Electronics"
                else (
                    f"Efficient and stylish {name.lower()} for your home"
                    if category == "Home & Kitchen"
                    else (
                        f"Bestselling {name.lower()} that will captivate readers"
                        if category == "Books"
                        else (
                            f"Comfortable and fashionable {name.lower()} for all occasions"
                            if category == "Clothing"
                            else f"High-performance {name.lower()} for sports enthusiasts"
                        )
                    )
                )
            ),
            price=round(random.uniform(price_range[0], price_range[1]), 2),
            stock=random.randint(10, 200),
        )
        for category, items in categories.items()
        for i, (name, *price_range) in enumerate(items, 1)
    ]

    db.add_all(items)
    db.commit()

    customer_ids = [f"customer{i}" for i in range(1, 11)]
    order_statuses = list(OrderStatus)

    orders = [
        Order(
            customer_id=random.choice(customer_ids),
            total_amount=round(
                sum(
                    item.price * random.randint(1, 5)
                    for item in random.sample(items, random.randint(1, 5))
                ),
                2,
            ),
            status=random.choice(order_statuses),
            created_at=datetime.now() - timedelta(days=random.randint(0, 30)),
            items=[
                OrderItem(item_id=item.id, quantity=random.randint(1, 5))
                for item in random.sample(items, random.randint(1, 5))
            ],
        )
        for _ in range(25)
    ]

    db.add_all(orders)
    db.commit()


# Call the seed_database function when the app starts
@app.on_event("startup")
async def startup_event():
    seed_database()
