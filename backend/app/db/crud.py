from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
import typing as t

from . import models, schemas
from app.core.security import get_password_hash

from pprint import pprint


def create_post(db: Session, post: schemas.PostCreate):
    db_post = models.Post(
        title=post.title,
        user_id=post.user_id,
        image_url=post.image_url,
        source_url=post.source_url,
        content=post.content,
    )
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


def delete_post(db: Session, post_id: int, current_user):
    response = get_post(db, post_id)
    if not response:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Post not found")
    post, user, *_ = response
    if post.user_id != current_user.id:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Not a post owner")
    db.delete(post)
    db.commit()
    return True


def update_post(db, fields_to_update, **kwargs):
    post_id = kwargs.get('post_id')
    user_id = kwargs.get('user_id')
    response = get_post(db, post_id)
    if not response:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Post not found")
    post, user, *_ = response
    if post.user_id != user_id:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Not a post owner")

    for key, value in fields_to_update.items():
        setattr(post, key, value)

    db.add(post)
    db.commit()
    db.refresh(post)
    return (post, user)


def get_post(db: Session, post_id: int):
    response = db.query(
            models.Post,
            models.User,
            func.count(models.Like.rating).filter(models.Like.rating == 1).label('good'),
            func.count(models.Like.rating).filter(models.Like.rating == -1).label('bad')
        ).filter(models.Post.id == post_id).join(models.User, models.User.id == models.Post.user_id) \
        .outerjoin(models.Like, models.Like.post_id == models.Post.id) \
        .group_by(models.User.id, models.Post.id).first()
    if not response:
        raise HTTPException(status_code=404, detail="Post not found")
    return response


def get_user_post_rating(db: Session, post_id: int, user_id: int):
    db_like = db.query(models.Like.rating) \
        .filter(models.Like.user_id == user_id and models.Like.post_id == post_id) \
        .first()
    if not db_like:
        return 0
    return db_like[0]


def get_posts(db: Session, skip: int = 0, limit: int = 100):
    result =  db.query(
            models.Post,
            models.User,
            func.count(models.Like.rating).filter(models.Like.rating == 1).label('good'),
            func.count(models.Like.rating).filter(models.Like.rating == -1).label('bad')
        ).join(models.User, models.User.id == models.Post.user_id) \
        .outerjoin(models.Like, models.Like.post_id == models.Post.id) \
        .group_by(models.User.id, models.Post.id).order_by(models.Post.created).offset(skip).limit(limit).all()
    print(result)
    return result


def get_user(db: Session, user_id: int):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def get_user_by_email(db: Session, email: str) -> schemas.UserBase:
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(
    db: Session, skip: int = 0, limit: int = 100
) -> t.List[schemas.UserOut]:
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        is_active=user.is_active,
        is_superuser=user.is_superuser,
        hashed_password=hashed_password,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int):
    user = get_user(db, user_id)
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="User not found")
    db.delete(user)
    db.commit()
    return user


def edit_user(
    db: Session, user_id: int, user: schemas.UserEdit
) -> schemas.User:
    db_user = get_user(db, user_id)
    if not db_user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="User not found")
    update_data = user.dict(exclude_unset=True)

    if "password" in update_data:
        update_data["hashed_password"] = get_password_hash(user.password)
        del update_data["password"]

    for key, value in update_data.items():
        setattr(db_user, key, value)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def rate_post(db: Session, like: schemas.LikeCreate) -> schemas.BaseLike:
    db_like = db.query(models.Like) \
        .filter(models.Like.user_id == like.user_id and models.Like.post_id == like.post_id) \
        .first()
    if not db_like:
        db_like = models.Like(
            user_id=like.user_id,
            post_id=like.post_id,
            rating=like.rating
        )
    else:
        if db_like.rating == like.rating:
            db.delete(db_like)
            db.commit()
            response_like = schemas.BaseLike(rating=0)
            print(response_like)
            return response_like
        else:
            db_like.rating = like.rating
    print(db_like)
    db.add(db_like)
    db.commit()
    db.refresh(db_like)
    print(db_like)
    return db_like
