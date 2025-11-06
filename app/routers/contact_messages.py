from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import Response
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import ContactMessage
from app.schemas import ContactMessageCreate, ContactMessageStatusUpdate, ContactMessageResponse
from app.auth import get_current_user_from_session

router = APIRouter()


@router.get("/contact-messages", response_model=List[ContactMessageResponse])
async def get_contact_messages(
    request: Request,
    db: Session = Depends(get_db),
):
    """Get all contact messages (auth required)"""
    get_current_user_from_session(request, db)  # Check authentication
    
    messages = db.query(ContactMessage).order_by(ContactMessage.created_at.desc()).all()
    return messages


@router.post("/contact")
async def create_contact_message(
    message_data: ContactMessageCreate,
    db: Session = Depends(get_db),
):
    """Create a new contact message"""
    new_message = ContactMessage(
        name=message_data.name,
        email=message_data.email,
        company=message_data.company,
        message=message_data.message,
        status="new",
    )
    db.add(new_message)
    db.commit()
    db.refresh(new_message)
    return Response(status_code=status.HTTP_200_OK)


@router.patch("/contact-messages/{message_id}/status")
async def update_contact_message_status(
    message_id: str,
    status_data: ContactMessageStatusUpdate,
    request: Request,
    db: Session = Depends(get_db),
):
    """Update contact message status (auth required)"""
    get_current_user_from_session(request, db)  # Check authentication
    
    message = db.query(ContactMessage).filter(ContactMessage.id == message_id).first()
    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contact message not found",
        )
    
    message.status = status_data.status
    db.commit()
    return Response(status_code=status.HTTP_200_OK)


@router.delete("/contact-messages/{message_id}")
async def delete_contact_message(
    message_id: str,
    request: Request,
    db: Session = Depends(get_db),
):
    """Delete a contact message (auth required)"""
    get_current_user_from_session(request, db)  # Check authentication
    
    message = db.query(ContactMessage).filter(ContactMessage.id == message_id).first()
    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contact message not found",
        )
    
    db.delete(message)
    db.commit()
    return Response(status_code=status.HTTP_200_OK)

