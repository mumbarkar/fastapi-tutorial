# Load required libraries
from fastapi import FastAPI

# Initialize the FastAPI app
app = FastAPI()

# Define a route for the root endpoint
@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

products = [
    {"id": 1, "name": "phone", "description": "This is a smartphone", "price": 10.0, "quantity": 100},
    {"id": 2, "name": "laptop", "description": "This is a laptop", "price": 20.0, "quantity": 50},
    {"id": 3, "name": "tablet", "description": "This is a tablet", "price": 30.0, "quantity": 25},
    {"id": 4, "name": "watch", "description": "This is a watch", "price": 40.0, "quantity": 10}
]

@app.get("/products")
def get_products():
    return products

@app.get("/product/{id}")
def get_product(id: int):
    for product in products:
        if product["id"] == id:
            return product
    return {"message": "Product not found"}