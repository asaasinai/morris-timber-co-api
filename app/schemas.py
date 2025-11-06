from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


# User Schemas
class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str


class UserResponse(UserBase):
    id: str
    password: str  # Note: In production, you might want to exclude this

    class Config:
        from_attributes = True


# Product Schemas
class ProductBase(BaseModel):
    name: str
    species: str
    dimensions: str
    origin: str
    story: str
    image: str
    category: str
    display_order: int = Field(default=0, alias="displayOrder")

    class Config:
        populate_by_name = True


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    species: Optional[str] = None
    dimensions: Optional[str] = None
    origin: Optional[str] = None
    story: Optional[str] = None
    image: Optional[str] = None
    category: Optional[str] = None
    display_order: Optional[int] = Field(None, alias="displayOrder")

    class Config:
        populate_by_name = True


class ProductResponse(ProductBase):
    id: str

    class Config:
        from_attributes = True
        populate_by_name = True  # Allow both snake_case and camelCase


# Team Member Schemas
class TeamMemberBase(BaseModel):
    name: str
    title: str
    bio: str
    image: str
    display_order: int = Field(default=0, alias="displayOrder")

    class Config:
        populate_by_name = True


class TeamMemberCreate(TeamMemberBase):
    pass


class TeamMemberUpdate(BaseModel):
    name: Optional[str] = None
    title: Optional[str] = None
    bio: Optional[str] = None
    image: Optional[str] = None
    display_order: Optional[int] = Field(None, alias="displayOrder")

    class Config:
        populate_by_name = True


class TeamMemberResponse(TeamMemberBase):
    id: str

    class Config:
        from_attributes = True
        populate_by_name = True


# Story Panel Schemas
class StoryPanelBase(BaseModel):
    title: str
    description: str
    image: str
    display_order: int = Field(default=0, alias="displayOrder")

    class Config:
        populate_by_name = True


class StoryPanelCreate(StoryPanelBase):
    pass


class StoryPanelUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    image: Optional[str] = None
    display_order: Optional[int] = Field(None, alias="displayOrder")

    class Config:
        populate_by_name = True


class StoryPanelResponse(StoryPanelBase):
    id: str

    class Config:
        from_attributes = True
        populate_by_name = True


# Site Settings Schemas
class SiteSettingsBase(BaseModel):
    hero_title: str = Field(alias="heroTitle")
    hero_subtitle: str = Field(alias="heroSubtitle")
    hero_image: str = Field(alias="heroImage")
    mission_title: str = Field(alias="missionTitle")
    mission_description: str = Field(alias="missionDescription")
    contact_phone: str = Field(alias="contactPhone")
    contact_email: Optional[str] = Field(None, alias="contactEmail")

    class Config:
        populate_by_name = True


class SiteSettingsUpdate(BaseModel):
    hero_title: Optional[str] = Field(None, alias="heroTitle")
    hero_subtitle: Optional[str] = Field(None, alias="heroSubtitle")
    hero_image: Optional[str] = Field(None, alias="heroImage")
    mission_title: Optional[str] = Field(None, alias="missionTitle")
    mission_description: Optional[str] = Field(None, alias="missionDescription")
    contact_phone: Optional[str] = Field(None, alias="contactPhone")
    contact_email: Optional[str] = Field(None, alias="contactEmail")

    class Config:
        populate_by_name = True


class SiteSettingsResponse(SiteSettingsBase):
    id: str

    class Config:
        from_attributes = True
        populate_by_name = True


# Contact Message Schemas
class ContactMessageBase(BaseModel):
    name: str
    email: str
    company: Optional[str] = None
    message: str


class ContactMessageCreate(ContactMessageBase):
    pass


class ContactMessageStatusUpdate(BaseModel):
    status: str


class ContactMessageResponse(ContactMessageBase):
    id: str
    created_at: datetime = Field(alias="createdAt")
    status: str

    class Config:
        from_attributes = True
        populate_by_name = True


# Login Schema
class LoginRequest(BaseModel):
    username: str
    password: str

