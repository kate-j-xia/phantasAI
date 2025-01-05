
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

from core.db import SessionLocal
import core.schema as models

# Pydantic models for request/response validation
class UserBase(BaseModel):    
    name: str
    date: datetime

class ArtBase(BaseModel):
    prompt: str
    summary: Optional[str] = None
    image: Optional[str] = None
    timestamp: datetime

class ArtResp(ArtBase):
    id: int
    
    class Config():
        orm_mode = True

class UserResp(UserBase):
    id: int
    arts: List[ArtResp]

    class Config():
        orm_mode = True

class UserListResp(BaseModel):
    id: int
    name: str
    date: str
    
# Create a session instance
def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()

def create_user(db_session, name: str):
    user = models.User(name=name)
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user

def create_art(db_session, user_id: int, prompt: str, summary: str, image: str, status: str):
    art = models.Art(user_id=user_id, prompt=prompt, summary=summary, image=image, status=status)
    db_session.add(art)
    db_session.commit()
    db_session.refresh(art)
    return art

def get_users(db_session):
    users = db_session.query(models.User).all()
    print(f'get_users(): got {len(users)} users.')
    return users

# Get user's arts by username
def get_arts_by_user(db_session, user_name: str):
    user = db_session.query(models.User).filter(models.User.name == user_name).first()
    if user:
        return {"user": user, "arts": user.arts}
    return None


