from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, unique=True, nullable=False)
    name = Column(String)
    password = Column(String, nullable=False)
    plan_type = Column(String, default='free')
    created_at = Column(DateTime, default=datetime.utcnow)

class Profile(Base):
    __tablename__ = "profiles"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    display_name = Column(String)
    avatar_url = Column(String)
    bio = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

class Journal(Base):
    __tablename__ = "journals"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class Mood(Base):
    __tablename__ = "moods"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    mood = Column(Integer, nullable=False)
    note = Column(Text)
    recorded_at = Column(DateTime, default=datetime.utcnow)

class UsageCount(Base):
    __tablename__ = "usage_counts"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    feature_type = Column(String, nullable=False)
    usage_count = Column(Integer, default=0)
    reset_date = Column(DateTime, default=datetime.utcnow)

class FeatureLimit(Base):
    __tablename__ = "feature_limits"
    id = Column(Integer, primary_key=True, autoincrement=True)
    feature_type = Column(String, nullable=False)
    plan_type = Column(String, nullable=False)
    monthly_limit = Column(Integer, nullable=False) 