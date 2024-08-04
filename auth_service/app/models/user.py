# auth_service/app/models/user.py

from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime, timedelta, timezone
from app.database import Base
import random

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    verification_code = Column(String, nullable=True)
    verification_code_expiry = Column(DateTime, nullable=True)

    def set_verification_code(self):
        code = random.randint(100000, 999999)
        self.verification_code = str(code)
        self.verification_code_expiry = datetime.now(timezone.utc) + timedelta(minutes=60)