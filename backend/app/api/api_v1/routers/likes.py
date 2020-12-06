from fastapi import APIRouter, Depends, HTTPException, status, Response, Request
from app.db.schemas import BaseLike, LikeCreate
import typing as t 

from app.db.session import get_db
from app.db.crud import (
    rate_post    
)
from app.core.auth import get_current_active_user

like_router = r = APIRouter()


@r.post(
    "/like/{post_id}",
    response_model=BaseLike,
    response_model_exclude_none=True
)
async def like_post(
    request: Request,
    post_id: int,
    like: BaseLike,
    db=Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    """
    Get specyfic post
    """
    new_like = LikeCreate(
        user_id=current_user.id,
        post_id=post_id,
        rating=like.rating
    )
    ret = rate_post(db, new_like)
    print(ret)
    return ret
