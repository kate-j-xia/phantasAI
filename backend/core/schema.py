from core.db import Base, engine
from sqlalchemy import Column, String, Integer, Float, Boolean, Text, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    date = Column(DateTime(timezone=True), server_default=func.now())

    # Relationship to Arts
    arts = relationship("Art", back_populates="user")

class Art(Base):
    __tablename__ = "arts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    prompt = Column(Text, nullable=False)
    summary = Column(Text)
    image = Column(String)  # Path or URL to the image
    like = Column(Boolean)
    status = Column(Text) # In Progress, Done, Invalid, Deleted
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationship to Users
    user = relationship("User", back_populates="arts")

# Create all tables
Base.metadata.create_all(bind=engine)    