from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import SiteSettings
from app.schemas import SiteSettingsUpdate, SiteSettingsResponse
from app.auth import get_current_user_from_session

router = APIRouter()


@router.get("/site-settings", response_model=SiteSettingsResponse)
async def get_site_settings(db: Session = Depends(get_db)):
    """Get site settings"""
    settings = db.query(SiteSettings).first()
    if not settings:
        # Create default settings if none exist
        default_settings = SiteSettings(
            hero_title="Welcome to Morris Timber Co",
            hero_subtitle="Premium Timber Products",
            hero_image="",
            mission_title="Our Mission",
            mission_description="Delivering quality timber products",
            contact_phone="",
            contact_email=None,
        )
        db.add(default_settings)
        db.commit()
        db.refresh(default_settings)
        return default_settings
    return settings


@router.patch("/site-settings", response_model=SiteSettingsResponse)
async def update_site_settings(
    settings_data: SiteSettingsUpdate,
    request: Request,
    db: Session = Depends(get_db),
):
    """Update site settings (auth required)"""
    get_current_user_from_session(request, db)  # Check authentication
    
    settings = db.query(SiteSettings).first()
    if not settings:
        # Create new settings if none exist
        settings = SiteSettings(
            hero_title="",
            hero_subtitle="",
            hero_image="",
            mission_title="",
            mission_description="",
            contact_phone="",
            contact_email=None,
        )
        db.add(settings)
        db.commit()
        db.refresh(settings)
    
    # Update only provided fields
    # by_alias=False gives us snake_case field names for database
    update_data = settings_data.model_dump(exclude_unset=True, by_alias=False)
    for field, value in update_data.items():
        setattr(settings, field, value)
    
    db.commit()
    db.refresh(settings)
    return settings

