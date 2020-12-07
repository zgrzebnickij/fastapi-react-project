from fastapi import APIRouter, Depends, HTTPException, status, Response, Form, File, UploadFile, Request
from app.db.schemas import PostCreate, Post, User, PostBase, PostLike, PostWithLikes
import typing as t

from app.db.session import get_db
from app.db.crud import (
    get_users,
    get_user,
    create_user,
    delete_user,
    edit_user,
    create_post,
    update_post,
    get_post,
    get_posts,
    delete_post,
    get_user_post_rating
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
    response_model=PostWithLikes
)
async def post_detail(
    request: Request,
    post_id: int,
    db=Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    """
    Get specyfic post
    """
    print(post_id)
    post, user, *likes = get_post(db, post_id)
    print(likes)
    return PostWithLikes(
        id=post.id,
        title=post.title,
        user_id=post.user_id,
        image_url=post.image_url,
        source_url=post.source_url,
        content=post.content,
        created=post.created.isoformat(),
        user=user,
        likes=PostLike(
            plus=likes[0],
            minus=likes[1],
            my_rate=get_user_post_rating(db, post.id, current_user.id)
            )
        )


@r.get(
    "/posts",
    response_model=t.List[PostWithLikes]
)
async def posts_details(
    request: Request,
    db=Depends(get_db),
    current_user=Depends(get_current_active_user)
):
    """
    Get specyfic post
    """
    posts = get_posts(db)
    print(posts)
    return [PostWithLikes(
        id=post.id,
        title=post.title,
        user_id=post.user_id,
        image_url=post.image_url,
        source_url=post.source_url,
        content=post.content,
        created=post.created.isoformat(),
        user=user,
        likes=PostLike(
            plus=likes[0],
            minus=likes[1],
            my_rate=get_user_post_rating(db, post.id, current_user.id)
            )
        ) for post, user, *likes in posts]


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


@r.put(
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
        title=title,
        user_id=current_user.id,
        source_url=source_url,
        content=content,
        image_url=image_name,
    )
    print(post)
    return create_post(db, post)


@r.post(
    "/posts/{post_id}",
    response_model=Post,
)
async def post_update(
    response: Response,
    post_id: int,
    db=Depends(get_db),
    current_user=Depends(get_current_active_user),
    source_url: t.Optional[str] = Form(None),
    title: t.Optional[str] = Form(None),
    content: t.Optional[str] = Form(None),
    image: t.Optional[UploadFile] = File(None),
):
    """
    Post update
    """
    fields_to_update = {}
    if title:
        fields_to_update['title'] = title
    if source_url:
        fields_to_update['source_url'] = source_url
    if content:
        fields_to_update['content'] = content
    if image:
        image_content = await image.read()
        image_name = save_post_image(image.filename, image_content)
        fields_to_update['image_url'] = image_name
    post, user = update_post(db, fields_to_update,
                             post_id=post_id, user_id=current_user.id)
    return Post(
        id=post.id,
        title=post.title,
        user_id=post.user_id,
        image_url=post.image_url,
        source_url=post.source_url,
        content=post.content,
        created=post.created.isoformat(),
        user=user)
