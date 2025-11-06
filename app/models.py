from sqlalchemy import Column, String, Integer, DateTime, Text
from sqlalchemy.sql import func
from app.database import Base
import uuid


def generate_id():
    return str(uuid.uuid4())


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=generate_id)
    username = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)  # Will store hashed password


class Product(Base):
    __tablename__ = "products"

    id = Column(String, primary_key=True, default=generate_id)
    name = Column(String, nullable=False)
    species = Column(String, nullable=False)
    dimensions = Column(String, nullable=False)
    origin = Column(String, nullable=False)
    story = Column(Text, nullable=False)
    image = Column(String, nullable=False)
    category = Column(String, nullable=False)
    display_order = Column(Integer, default=0)


class TeamMember(Base):
    __tablename__ = "team_members"

    id = Column(String, primary_key=True, default=generate_id)
    name = Column(String, nullable=False)
    title = Column(String, nullable=False)
    bio = Column(Text, nullable=False)
    image = Column(String, nullable=False)
    display_order = Column(Integer, default=0)


class StoryPanel(Base):
    __tablename__ = "story_panels"

    id = Column(String, primary_key=True, default=generate_id)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    image = Column(String, nullable=False)
    display_order = Column(Integer, default=0)


class SiteSettings(Base):
    __tablename__ = "site_settings"

    id = Column(String, primary_key=True, default=generate_id)
    hero_title = Column(String, nullable=False)
    hero_subtitle = Column(String, nullable=False)
    hero_image = Column(String, nullable=False)
    mission_title = Column(String, nullable=False)
    mission_description = Column(Text, nullable=False)
    contact_phone = Column(String, nullable=False)
    contact_email = Column(String, nullable=True)


class ContactMessage(Base):
    __tablename__ = "contact_messages"

    id = Column(String, primary_key=True, default=generate_id)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    company = Column(String, nullable=True)
    message = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    status = Column(String, default="new")  # new, read, replied, archived

