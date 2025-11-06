from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import Response
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import TeamMember
from app.schemas import TeamMemberCreate, TeamMemberUpdate, TeamMemberResponse
from app.auth import get_current_user_from_session

router = APIRouter()


@router.get("/team-members", response_model=List[TeamMemberResponse])
async def get_team_members(db: Session = Depends(get_db)):
    """Get all team members"""
    team_members = db.query(TeamMember).order_by(TeamMember.display_order).all()
    return team_members


@router.post("/team-members", response_model=TeamMemberResponse, status_code=status.HTTP_201_CREATED)
async def create_team_member(
    team_member_data: TeamMemberCreate,
    request: Request,
    db: Session = Depends(get_db),
):
    """Create a new team member (auth required)"""
    get_current_user_from_session(request, db)  # Check authentication
    
    new_team_member = TeamMember(**team_member_data.model_dump(by_alias=False))
    db.add(new_team_member)
    db.commit()
    db.refresh(new_team_member)
    return new_team_member


@router.patch("/team-members/{team_member_id}", response_model=TeamMemberResponse)
async def update_team_member(
    team_member_id: str,
    team_member_data: TeamMemberUpdate,
    request: Request,
    db: Session = Depends(get_db),
):
    """Update a team member (auth required)"""
    get_current_user_from_session(request, db)  # Check authentication
    
    team_member = db.query(TeamMember).filter(TeamMember.id == team_member_id).first()
    if not team_member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Team member not found",
        )
    
    # Update only provided fields
    update_data = team_member_data.model_dump(exclude_unset=True, by_alias=False)
    for field, value in update_data.items():
        setattr(team_member, field, value)
    
    db.commit()
    db.refresh(team_member)
    return team_member


@router.delete("/team-members/{team_member_id}")
async def delete_team_member(
    team_member_id: str,
    request: Request,
    db: Session = Depends(get_db),
):
    """Delete a team member (auth required)"""
    get_current_user_from_session(request, db)  # Check authentication
    
    team_member = db.query(TeamMember).filter(TeamMember.id == team_member_id).first()
    if not team_member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Team member not found",
        )
    
    db.delete(team_member)
    db.commit()
    return Response(status_code=status.HTTP_200_OK)

