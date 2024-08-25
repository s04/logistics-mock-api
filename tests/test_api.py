import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.models.database import SessionLocal, Base, engine
from app.models.item import Item
from app.models.order import Order, OrderItem, OrderStatus

client = TestClient(app)


@pytest.fixture(scope="module")
def setup_database():
    # Create the database and tables
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    # Seed the database with initial data
    items = [
        Item(name="Test Item 1", description="A test item", price=10.0, stock=100),
        Item(
            name="Test Item 2", description="Another test item", price=20.0, stock=200
        ),
    ]
    db.add_all(items)
    db.commit()

    yield db

    # Drop the database tables after tests
    Base.metadata.drop_all(bind=engine)
    db.close()


def test_list_items(setup_database):
    response = client.get("/items")
    assert response.status_code == 200
    assert len(response.json()) > 0


def test_create_item(setup_database):
    response = client.post(
        "/items",
        json={
            "name": "New Item",
            "description": "A new item",
            "price": 15.0,
            "stock": 50,
        },
    )
    assert response.status_code == 201
    assert response.json()["name"] == "New Item"


def test_get_item(setup_database):
    response = client.get("/items/1")
    assert response.status_code == 200
    assert response.json()["name"] == "Test Item 1"


def test_update_item(setup_database):
    response = client.put(
        "/items/1",
        json={
            "name": "Updated Item",
            "description": "An updated item",
            "price": 12.0,
            "stock": 80,
        },
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Updated Item"


def test_delete_item(setup_database):
    response = client.delete("/items/1")
    assert response.status_code == 204


def test_list_orders(setup_database):
    response = client.get("/orders")
    assert response.status_code == 200
    assert len(response.json()) >= 0


def test_create_order(setup_database):
    response = client.post(
        "/orders",
        json={"customer_id": "customer1", "items": [{"item_id": 2, "quantity": 1}]},
    )
    assert response.status_code == 201
    assert response.json()["customer_id"] == "customer1"


def test_get_order(setup_database):
    response = client.get("/orders/1")
    assert response.status_code == 200
    assert response.json()["customer_id"] == "customer1"


def test_update_order(setup_database):
    response = client.put("/orders/1", json={"status": "shipped"})
    assert response.status_code == 200
    assert response.json()["status"] == "shipped"


def test_delete_order(setup_database):
    response = client.delete("/orders/1")
    assert response.status_code == 204
