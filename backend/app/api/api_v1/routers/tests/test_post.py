from app.db import models
from pprint import pprint


def test_get_post(client, test_post, test_user, user_token_headers):
    response = client.get(
        f"/api/v1/posts/{test_post.id}",
        headers=user_token_headers
    )
    assert response.status_code == 200
    print(response.json())
    post = {
        'id': test_post.id,
        'title': test_post.title,
        'user_id': test_post.user_id,
        'image_url': test_post.image_url,
        'source_url': test_post.source_url,
        'content': test_post.content,
        'created': test_post.created.isoformat(),
        'user': {
            'id': test_user.id,
            'first_name': test_user.first_name,
            'last_name': test_user.last_name,
        }
    }
    print(post)
    assert response.json() == post


def test_get_posts(client, test_post, test_user, test_user_2, test_post_2, user_token_headers):
    response = client.get(
        "/api/v1/posts",
        headers=user_token_headers
    )
    print(response.json())
    assert response.status_code == 200
    posts = []
    for _test_post, _test_user in [(test_post, test_user), (test_post_2, test_user_2)]:
        post = {
            'id': _test_post.id,
            'title': _test_post.title,
            'user_id': _test_post.user_id,
            'image_url': _test_post.image_url,
            'source_url': _test_post.source_url,
            'content': _test_post.content,
            'created': _test_post.created.isoformat(),
            'user': {
                'id': _test_user.id,
                'first_name': _test_user.first_name,
                'last_name': _test_user.last_name,
            }
        }
        posts.append(post)
    pprint(posts)
    pprint(response.json())
    assert response.json() == posts


def test_delete_post(client, test_post, test_db, user_token_headers):
    response = client.delete(
        f"/api/v1/posts/{test_post.id}", headers=user_token_headers
    )
    assert response.status_code == 200
    assert test_db.query(models.Post).all() == []


def test_delete_post_not_found(client, superuser_token_headers):
    response = client.delete(
        "/api/v1/posts/4321", headers=superuser_token_headers
    )
    assert response.status_code == 404


# def test_edit_post(client, test_superuser, superuser_token_headers):
#     new_post = {
#         "email": "newemail@email.com",
#         "is_active": False,
#         "is_superuser": True,
#         "first_name": "Joe",
#         "last_name": "Smith",
#         "password": "new_password",
#     }

#     response = client.put(
#         f"/api/v1/users/{test_superuser.id}",
#         json=new_user,
#         headers=superuser_token_headers,
#     )
#     assert response.status_code == 200
#     new_user["id"] = test_superuser.id
#     new_user.pop("password")
#     assert response.json() == new_user


# def test_edit_user_not_found(client, test_db, superuser_token_headers):
#     new_user = {
#         "email": "newemail@email.com",
#         "is_active": False,
#         "is_superuser": False,
#         "password": "new_password",
#     }
#     response = client.put(
#         "/api/v1/users/1234", json=new_user, headers=superuser_token_headers
#     )
#     assert response.status_code == 404
