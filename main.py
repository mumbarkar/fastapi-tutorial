# Load required libraries
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from models import Product
from database import session, engine
import db_models
from sqlalchemy.orm import Session

# Initialize the FastAPI app
app = FastAPI()

# Configure CORS middleware to allow requests from the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Adjust this to your frontend URL
    allow_methods=["*"]
)

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

# Dependency to get a database session
def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()
        
# function to initialize the database with initial data
def init_db():
    db = session()
    count = db.query(db_models.Product).count()
    
    if count == 0:
        for product in products:
            db.add(db_models.Product(**product))
        db.commit()
    
# call the init_db function to populate the database with initial data
init_db()

# Get all products
@app.get("/products")
def get_products(db: Session = Depends(get_db)):
    db_products = db.query(db_models.Product).all()
    return db_products

# Get a product by its ID
@app.get("/products/{id}")
def get_product(id: int, db: Session = Depends(get_db)):
    db_product = db.query(db_models.Product).filter(db_models.Product.id == id).first()
    
    if db_product:
        return db_product
    
    return {"message": "Product not found"}

# Add a new product to the list
@app.post("/products")
def add_product(product: Product, db: Session = Depends(get_db)):
    db_product = db_models.Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

# Update an existing product
@app.put("/products/{id}")
def update_product(id: int, product: Product, db: Session = Depends(get_db)):
    db_product = db.query(db_models.Product).filter(db_models.Product.id == id).first()
    if not db_product:
        return {"message": "Product not found"}
    for key, value in product.dict().items():
        setattr(db_product, key, value)
    db.commit()
    db.refresh(db_product)
    return {"message": "Product updated successfully", "product": db_product}

# Delete a product
@app.delete("/products/{id}")
def delete_product(id: int, db: Session = Depends(get_db)):
    db_product = db.query(db_models.Product).filter(db_models.Product.id == id).first()
    if not db_product:
        return {"message": "Product not found"}
    db.delete(db_product)
    db.commit()
    return {"message": "Product deleted successfully"}