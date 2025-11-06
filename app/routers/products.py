from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import Response
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import Product
from app.schemas import ProductCreate, ProductUpdate, ProductResponse
from app.auth import get_current_user_from_session

router = APIRouter()


@router.get("/products", response_model=List[ProductResponse])
async def get_products(db: Session = Depends(get_db)):
    """Get all products"""
    products = db.query(Product).order_by(Product.display_order).all()
    return products


@router.post("/products", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product(
    product_data: ProductCreate,
    request: Request,
    db: Session = Depends(get_db),
):
    """Create a new product (auth required)"""
    get_current_user_from_session(request, db)  # Check authentication
    
    new_product = Product(**product_data.model_dump(by_alias=False))
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product


@router.patch("/products/{product_id}", response_model=ProductResponse)
async def update_product(
    product_id: str,
    product_data: ProductUpdate,
    request: Request,
    db: Session = Depends(get_db),
):
    """Update a product (auth required)"""
    get_current_user_from_session(request, db)  # Check authentication
    
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )
    
    # Update only provided fields
    update_data = product_data.model_dump(exclude_unset=True, by_alias=False)
    for field, value in update_data.items():
        setattr(product, field, value)
    
    db.commit()
    db.refresh(product)
    return product


@router.delete("/products/{product_id}")
async def delete_product(
    product_id: str,
    request: Request,
    db: Session = Depends(get_db),
):
    """Delete a product (auth required)"""
    get_current_user_from_session(request, db)  # Check authentication
    
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )
    
    db.delete(product)
    db.commit()
    return Response(status_code=status.HTTP_200_OK)

