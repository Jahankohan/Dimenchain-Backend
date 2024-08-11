# user_management_service/app/models/subscription.py

from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship 
from app.database import Base

class Subscription(Base):
    __tablename__ = "subscriptions"

    subscription_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user_profiles.user_id"), nullable=False)
    channel_id = Column(Integer, nullable=False)  # This would reference a channel in another service
    status = Column(String, nullable=False)  # 'active', 'canceled', 'pending'.
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationship to UserProfile
    user = relationship("UserProfile", back_populates="subscriptions")
