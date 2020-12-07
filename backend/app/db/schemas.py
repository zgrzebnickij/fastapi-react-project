from pydantic import BaseModel
import datetime
import typing as t


class PostLike(BaseModel):
    plus: int
    minus: int
    my_rate: int


class BaseLike(BaseModel):
    rating: int

    class Config:
        orm_mode = True


class LikeCreate(BaseLike):
    post_id: int
    user_id: int


class Like(LikeCreate):
    id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str
    is_active: bool = True
    is_superuser: bool = False
    first_name: str = None
    last_name: str = None


class UserPublic(BaseModel):
    first_name: str = None
    last_name: str = None
    id: int

    class Config:
        orm_mode = True


class PostBase(BaseModel):
    user_id: int
    source_url: str
    title: str
    content: str


class User(UserBase):
    id: int

    class Config:
        orm_mode = True


class PostCreate(PostBase):
    image_url: str


class Post(PostCreate):
    id: int
    created: datetime.datetime
    user: UserPublic

    class Config:
        orm_mode = True


class PostWithLikes(Post):
    likes: PostLike


class UserOut(UserBase):
    pass


class UserCreate(UserBase):
    password: str

    class Config:
        orm_mode = True


class UserEdit(UserBase):
    password: t.Optional[str] = None

    class Config:
        orm_mode = True


class User(UserBase):
    id: int

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str = None
    permissions: str = "user"
