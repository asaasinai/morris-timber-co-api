from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import Response
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import StoryPanel
from app.schemas import StoryPanelCreate, StoryPanelUpdate, StoryPanelResponse
from app.auth import get_current_user_from_session

router = APIRouter()


@router.get("/story-panels", response_model=List[StoryPanelResponse])
async def get_story_panels(db: Session = Depends(get_db)):
    """Get all story panels"""
    story_panels = db.query(StoryPanel).order_by(StoryPanel.display_order).all()
    return story_panels


@router.post("/story-panels", response_model=StoryPanelResponse, status_code=status.HTTP_201_CREATED)
async def create_story_panel(
    story_panel_data: StoryPanelCreate,
    request: Request,
    db: Session = Depends(get_db),
):
    """Create a new story panel (auth required)"""
    get_current_user_from_session(request, db)  # Check authentication
    
    new_story_panel = StoryPanel(**story_panel_data.model_dump(by_alias=False))
    db.add(new_story_panel)
    db.commit()
    db.refresh(new_story_panel)
    return new_story_panel


@router.patch("/story-panels/{story_panel_id}", response_model=StoryPanelResponse)
async def update_story_panel(
    story_panel_id: str,
    story_panel_data: StoryPanelUpdate,
    request: Request,
    db: Session = Depends(get_db),
):
    """Update a story panel (auth required)"""
    get_current_user_from_session(request, db)  # Check authentication
    
    story_panel = db.query(StoryPanel).filter(StoryPanel.id == story_panel_id).first()
    if not story_panel:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Story panel not found",
        )
    
    # Update only provided fields
    update_data = story_panel_data.model_dump(exclude_unset=True, by_alias=False)
    for field, value in update_data.items():
        setattr(story_panel, field, value)
    
    db.commit()
    db.refresh(story_panel)
    return story_panel


@router.delete("/story-panels/{story_panel_id}")
async def delete_story_panel(
    story_panel_id: str,
    request: Request,
    db: Session = Depends(get_db),
):
    """Delete a story panel (auth required)"""
    get_current_user_from_session(request, db)  # Check authentication
    
    story_panel = db.query(StoryPanel).filter(StoryPanel.id == story_panel_id).first()
    if not story_panel:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Story panel not found",
        )
    
    db.delete(story_panel)
    db.commit()
    return Response(status_code=status.HTTP_200_OK)

