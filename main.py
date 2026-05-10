# Load required libraries
from fastapi import FastAPI
from models import Product
from database import session, engine
import db_models

# Initialize the FastAPI app
app = FastAPI()

db_models.Base.metadata.create_all(bind=engine)

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

# function to initialize the database with initial data
def init_db():
    db = session()
    for product in products:
        db.add(db_models.Product(**product))
    db.commit()
    
# call the init_db function to populate the database with initial data
init_db()

# Get all products
@app.get("/products")
def get_products():
    return products
    # db connection
    # db = session()
    # query
    # db.query()

# Get a product by its ID
@app.get("/product/{id}")
def get_product(id: int):
    for product in products:
        if product["id"] == id:
            return product
    return {"message": "Product not found"}

# Add a new product to the list
@app.post("/product")
def add_product(product: Product):
    products.append(product)
    return {"message": "Product added successfully", "product": product}

# Update an existing product
@app.put("/product/{id}")
def update_product(id: int, product: Product):
    for i in range(len(products)):
        if products[i]["id"] == id:
            products[i] = product
            return {"message": "Product updated successfully", "product": product}
    return {"message": "Product not found"}

# Delete a product
@app.delete("/product/{id}")
def delete_product(id: int):
    global products
    for i in range(len(products)):
        if products[i]["id"] == id:
            del products[i]
            return {"message": "Product deleted successfully"}
    return {"message": "Product not found"}