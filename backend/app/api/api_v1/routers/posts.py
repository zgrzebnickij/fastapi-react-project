from fastapi import APIRouter, Depends, HTTPException, status, Response, Form, File, UploadFile, Request
from app.db.schemas import PostCreate, Post, User, PostBase
import typing as t 

from app.db.session import get_db
from app.db.crud import (
    get_users,
    get_user,
    create_user,
    delete_user,
    edit_user,
    create_post,
    get_post,
    get_posts,
    delete_post
)
from app.core.auth import get_current_active_user

from pprint import pprint
import uuid
import os

posts_router = r = APIRouter()


def save_post_image(filename, image):
    # todo: rescale to specyfic size
    # todo: correct path
    _, file_extension = os.path.splitext(filename)
    new_filename = uuid.uuid4().hex
    with open(f'/home/jakub/Documents/Projects/ModernStack/fastapi-react-project/pictures/posts/{new_filename}.{file_extension}', 'wb') as file:
        file.write(image)
    return new_filename


@r.get(
    "/posts/{post_id}",
    response_model=Post,
)
async def post_details(
    request: Request,
    post_id: int,
    db=Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    """
    Get specyfic post
    """
    print(post_id)
    post, user = get_post(db, post_id)
    return Post(
        id=post.id,
        title=post.title,
        user_id=post.user_id,
        image_url=post.image_url,
        source_url=post.source_url,
        content=post.content,
        created=post.created.isoformat(),
        user=user)


@r.get(
    "/posts",
    response_model=t.List[Post],
)
async def posts_details(
    request: Request,
    db=Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    """
    Get specyfic post
    """
    posts = get_posts(db)
    return [Post(
        id=post.id,
        title=post.title,
        user_id=post.user_id,
        image_url=post.image_url,
        source_url=post.source_url,
        content=post.content,
        created=post.created.isoformat(),
        user=user) for post, user in posts]


@r.delete(
    "/posts/{post_id}",
    response_model=bool
)
async def post_delete(
    request: Request,
    post_id: int,
    db=Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    """
    Get specyfic post
    """
    return delete_post(db, post_id, current_user)


@r.post(
    "/posts",
)
async def post_create(
    response: Response,
    db=Depends(get_db),
    current_user=Depends(get_current_active_user),
    source_url: str = Form(...),
    title: str = Form(...),
    content: str = Form(...),
    image: UploadFile = File(...),
):
    """
    Get all users
    """
    image_content = await image.read()
    image_name = save_post_image(image.filename, image_content)
    post = PostCreate(
        user_id=current_user.id,
        source_url=source_url,
        content=content,
        image_url=image_name,
    )
    return create_post(db, post)
