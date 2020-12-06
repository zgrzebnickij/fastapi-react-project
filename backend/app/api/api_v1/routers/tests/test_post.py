from app.db import models
from pprint import pprint
from io import StringIO

import os
import logging

requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = True


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


def test_add_post(client, test_user, user_token_headers):
    path = os.path.dirname(os.path.abspath(__file__))
    filename = 'test_static/test_img.jpg'
    file_path = os.path.join(path, filename)

    new_post = {
        'title': 'This is test post',
        'source_url': 'sourceUrl',
        'content': 'This is a content of test post, but test test if you know what...'
    }

    response = client.put(
        "/api/v1/posts",
        files={"image": open(file_path, "rb")},
        data=new_post,
        headers=user_token_headers,
    )
    pprint(response.content)
    pprint(response.headers)
    assert response.status_code == 200
    new_post["user_id"] = test_user.id

    resp = response.json()
    print({resp[key] == new_post[key] for key in ['title', 'content', 'source_url', 'user_id']})
    assert all(resp[key] == new_post[key] for key in ['title', 'content', 'source_url', 'user_id'])


def test_update_post(client, test_post, test_user, user_token_headers):

    updated_post = {
        'title': 'This is test post updated',
        'content': 'This is a content of test post updated, but test test if you know what...'
    }

    response = client.post(
        f"/api/v1/posts/{test_post.id}",
        data=updated_post,
        headers=user_token_headers,
    )
    pprint(response.content)
    pprint(response.headers)
    assert response.status_code == 200
    updated_post["user_id"] = test_user.id

    resp = response.json()
    print({resp[key] == updated_post[key] for key in [*updated_post.keys(), 'user_id']})
    assert all(resp[key] == updated_post[key] for key in [*updated_post.keys(), 'user_id'])
