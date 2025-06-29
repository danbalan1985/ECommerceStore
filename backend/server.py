from fastapi import FastAPI, APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field
from typing import List, Optional
import uuid
from datetime import datetime, timedelta
import jwt
import bcrypt
from bson import ObjectId

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Create the main app without a prefix
app = FastAPI()

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# JWT Configuration
SECRET_KEY = "your-secret-key-change-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

security = HTTPBearer()

# Pydantic Models
class User(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    email: str
    password: str
    full_name: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

class UserCreate(BaseModel):
    email: str
    password: str
    full_name: str

class UserLogin(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    id: str
    email: str
    full_name: str
    created_at: datetime

class Product(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    description: str
    price: float
    category: str
    image_url: str
    stock: int
    rating: float = 4.5
    created_at: datetime = Field(default_factory=datetime.utcnow)

class CartItem(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    product_id: str
    quantity: int
    created_at: datetime = Field(default_factory=datetime.utcnow)

class CartItemCreate(BaseModel):
    product_id: str
    quantity: int

class CartItemResponse(BaseModel):
    id: str
    product: Product
    quantity: int
    created_at: datetime

class Token(BaseModel):
    access_token: str
    token_type: str

# Utility functions
def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user = await db.users.find_one({"id": user_id})
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return User(**user)

# Initialize sample products
async def init_products():
    existing = await db.products.find_one()
    if existing:
        return
    
    products = [
        Product(name="iPhone 14 Pro", description="Latest iPhone with advanced camera system", price=999.99, category="smartphones", image_url="https://images.unsplash.com/photo-1589492477829-5e65395b66cc", stock=25),
        Product(name="MacBook Pro 16\"", description="Professional laptop with M2 chip", price=2499.99, category="laptops", image_url="https://images.unsplash.com/photo-1649972904349-6e44c42644a7", stock=15),
        Product(name="AirPods Pro", description="Premium wireless earbuds with noise cancellation", price=249.99, category="headphones", image_url="https://images.pexels.com/photos/14272792/pexels-photo-14272792.jpeg", stock=50),
        Product(name="Gaming Headset", description="High-quality gaming headphones", price=179.99, category="headphones", image_url="https://images.pexels.com/photos/3394650/pexels-photo-3394650.jpeg", stock=30),
        Product(name="Wireless Mouse", description="Ergonomic wireless mouse", price=79.99, category="accessories", image_url="https://images.unsplash.com/photo-1587749091716-f7b291a87f87", stock=40),
        Product(name="USB-C Cable", description="Fast charging USB-C cable", price=19.99, category="accessories", image_url="https://images.pexels.com/photos/914912/pexels-photo-914912.jpeg", stock=100),
        Product(name="Mechanical Keyboard", description="RGB mechanical gaming keyboard", price=149.99, category="accessories", image_url="https://images.pexels.com/photos/4491648/pexels-photo-4491648.jpeg", stock=20),
        Product(name="4K Webcam", description="Ultra HD webcam for streaming", price=199.99, category="accessories", image_url="https://images.unsplash.com/photo-1650958797279-1cc24e982c48", stock=15),
        Product(name="Smart Watch", description="Fitness tracking smartwatch", price=299.99, category="wearables", image_url="https://images.unsplash.com/photo-1612690669207-fed642192c40", stock=35),
        Product(name="Tablet Pro", description="Professional tablet with stylus", price=799.99, category="tablets", image_url="https://images.unsplash.com/photo-1656053418912-ae7b147d8168", stock=20),
        Product(name="Bluetooth Speaker", description="Portable wireless speaker", price=89.99, category="audio", image_url="https://images.pexels.com/photos/2259221/pexels-photo-2259221.jpeg", stock=45),
        Product(name="Phone Charger", description="Fast wireless phone charger", price=49.99, category="accessories", image_url="https://images.unsplash.com/photo-1492107376256-4026437926cd", stock=60),
        Product(name="Graphics Card", description="High-performance GPU for gaming", price=699.99, category="components", image_url="https://images.unsplash.com/photo-1558171813-8e717211582b", stock=10),
        Product(name="SSD Drive", description="1TB NVMe SSD storage", price=129.99, category="components", image_url="https://images.unsplash.com/photo-1490093158370-1a6be674437b", stock=25),
        Product(name="Monitor Stand", description="Adjustable monitor stand", price=59.99, category="accessories", image_url="https://images.pexels.com/photos/2259221/pexels-photo-2259221.jpeg", stock=30),
    ]
    
    for product in products:
        await db.products.insert_one(product.dict())

# Authentication routes
@api_router.post("/register", response_model=UserResponse)
async def register(user: UserCreate):
    existing = await db.users.find_one({"email": user.email})
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = hash_password(user.password)
    user_obj = User(email=user.email, password=hashed_password, full_name=user.full_name)
    await db.users.insert_one(user_obj.dict())
    return UserResponse(**user_obj.dict())

@api_router.post("/login", response_model=Token)
async def login(user: UserLogin):
    db_user = await db.users.find_one({"email": user.email})
    if not db_user or not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token = create_access_token(data={"sub": db_user["id"]})
    return {"access_token": access_token, "token_type": "bearer"}

@api_router.get("/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)):
    return UserResponse(**current_user.dict())

# Product routes
@api_router.get("/products", response_model=List[Product])
async def get_products(search: Optional[str] = None, category: Optional[str] = None):
    query = {}
    if search:
        query["$or"] = [
            {"name": {"$regex": search, "$options": "i"}},
            {"description": {"$regex": search, "$options": "i"}}
        ]
    if category:
        query["category"] = category
    
    products = await db.products.find(query).to_list(1000)
    return [Product(**product) for product in products]

@api_router.get("/products/{product_id}", response_model=Product)
async def get_product(product_id: str):
    product = await db.products.find_one({"id": product_id})
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return Product(**product)

@api_router.get("/categories")
async def get_categories():
    categories = await db.products.distinct("category")
    return {"categories": categories}

# Cart routes
@api_router.post("/cart", response_model=CartItemResponse)
async def add_to_cart(item: CartItemCreate, current_user: User = Depends(get_current_user)):
    product = await db.products.find_one({"id": item.product_id})
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    existing_item = await db.cart.find_one({"user_id": current_user.id, "product_id": item.product_id})
    if existing_item:
        new_quantity = existing_item["quantity"] + item.quantity
        await db.cart.update_one(
            {"id": existing_item["id"]}, 
            {"$set": {"quantity": new_quantity}}
        )
        existing_item["quantity"] = new_quantity
        return CartItemResponse(
            id=existing_item["id"],
            product=Product(**product),
            quantity=new_quantity,
            created_at=existing_item["created_at"]
        )
    
    cart_item = CartItem(user_id=current_user.id, product_id=item.product_id, quantity=item.quantity)
    await db.cart.insert_one(cart_item.dict())
    return CartItemResponse(
        id=cart_item.id,
        product=Product(**product),
        quantity=cart_item.quantity,
        created_at=cart_item.created_at
    )

@api_router.get("/cart", response_model=List[CartItemResponse])
async def get_cart(current_user: User = Depends(get_current_user)):
    cart_items = await db.cart.find({"user_id": current_user.id}).to_list(1000)
    result = []
    for item in cart_items:
        product = await db.products.find_one({"id": item["product_id"]})
        if product:
            result.append(CartItemResponse(
                id=item["id"],
                product=Product(**product),
                quantity=item["quantity"],
                created_at=item["created_at"]
            ))
    return result

@api_router.put("/cart/{item_id}")
async def update_cart_item(item_id: str, quantity: int, current_user: User = Depends(get_current_user)):
    result = await db.cart.update_one(
        {"id": item_id, "user_id": current_user.id},
        {"$set": {"quantity": quantity}}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Cart item not found")
    return {"message": "Cart updated"}

@api_router.delete("/cart/{item_id}")
async def remove_from_cart(item_id: str, current_user: User = Depends(get_current_user)):
    result = await db.cart.delete_one({"id": item_id, "user_id": current_user.id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Cart item not found")
    return {"message": "Item removed from cart"}

@api_router.delete("/cart")
async def clear_cart(current_user: User = Depends(get_current_user)):
    await db.cart.delete_many({"user_id": current_user.id})
    return {"message": "Cart cleared"}

# Initialize products on startup
@app.on_event("startup")
async def startup_event():
    await init_products()

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()