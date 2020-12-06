from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, DateTime

from .session import Base
import datetime


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)

    def __repr__(self):
        return "<User(namide='%s', name='%s', email='%s')>" % (
                                self.id, self.first_name, self.email)


class Post(Base):
    __tablename__ = "post"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(256))
    user_id = Column(Integer, ForeignKey('user.id'))
    image_url = Column(String, nullable=False)
    source_url = Column(String)
    content = Column(String)
    created = Column(DateTime, default=datetime.datetime.utcnow)


class Like(Base):
    __tablename__ = "like"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    post_id = Column(Integer, ForeignKey('post.id'))
    rating = Column(Integer, nullable=False)

    def __repr__(self):
        return "<Like(user_id='%s', post_id='%s', rating='%s')>" % (
                                self.user_id, self.post_id, self.rating)
