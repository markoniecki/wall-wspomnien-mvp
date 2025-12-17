from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime, timedelta
import secrets

from .db import Base

from sqlalchemy import Column, String, DateTime
from datetime import datetime

from sqlalchemy import Integer
from sqlalchemy import Column, Integer, String
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User", backref="events")

    token = Column(String, unique=True, index=True, nullable=False)
    admin_token = Column(String, unique=True, index=True, nullable=False)

    title = Column(String, nullable=False)
    organizer_email = Column(String, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=False)

    validity_minutes = Column(Integer, nullable=False, default=1440)  # 24h

    status = Column(String, default="active")

    # w klasie Event dodaj:
    pdf_path = Column(String, nullable=True)
    pdf_generated_at = Column(DateTime, nullable=True)
    pdf_sent_at = Column(DateTime, nullable=True)

    @staticmethod
    def create(title: str, organizer_email: str, validity_minutes: int):
        now = datetime.utcnow()
        return Event(
            title=title,
            organizer_email=organizer_email,
            token=secrets.token_urlsafe(16),
            admin_token=secrets.token_urlsafe(24),
            created_at=now,
            expires_at=now + timedelta(minutes=validity_minutes),
            validity_minutes=validity_minutes,
            status="active"
        )

    def is_expired(self) -> bool:
        return datetime.utcnow() > self.expires_at

    def close_if_expired(self):
        if self.is_expired() and self.status != "closed":
            self.status = "closed"

    def validity_label(self) -> str:
        minutes = self.validity_minutes

        if minutes < 60:
            return f"{minutes} minuta" if minutes == 1 else f"{minutes} minut"

        hours = minutes // 60

        if hours == 1:
            return "1 godzina"
        elif hours < 5:
            return f"{hours} godziny"
        else:
            return f"{hours} godzin"


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)

    author_name = Column(String, nullable=True)
    content = Column(Text, nullable=False)
    image_path = Column(String, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)

    event = relationship("Event", backref="posts")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)

    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)
