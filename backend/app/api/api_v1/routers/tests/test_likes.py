def test_like_post(client, test_post_2, test_user, user_token_headers):
    response = client.post(
        f"/api/v1/like/{test_post_2.id}",
        headers=user_token_headers,
        json={'rating': 1}
    )
    assert response.status_code == 200
    print(response.json())
    like = {
        'rating': 1,
    }
    print(like)
    assert response.json() == like


def test_like_post_2(client, test_post_2, test_user_2, user_token_headers):
    response = client.post(
        f"/api/v1/like/{test_post_2.id}",
        headers=user_token_headers,
        json={'rating': -1}
    )
    assert response.status_code == 200
    print(response.json())
    like = {
        'rating': -1,
    }
    print(like)
    assert response.json() == like
    response = client.get(
        f"/api/v1/posts/{test_post_2.id}",
        headers=user_token_headers
    )
    assert response.status_code == 200
    print(response.json())
    post = {
        'id': test_post_2.id,
        'title': test_post_2.title,
        'user_id': test_post_2.user_id,
        'image_url': test_post_2.image_url,
        'source_url': test_post_2.source_url,
        'content': test_post_2.content,
        'created': test_post_2.created.isoformat(),
        'user': {
            'id': test_user_2.id,
            'first_name': test_user_2.first_name,
            'last_name': test_user_2.last_name,
        },
        'likes': {
            'plus': 0,
            'minus': 1,
            'my_rate': -1,
        }
    }
    print(post)
    assert response.json() == post

