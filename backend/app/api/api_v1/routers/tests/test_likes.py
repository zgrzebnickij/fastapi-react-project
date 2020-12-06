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


def test_like_post_2(client, test_post_2, test_user, user_token_headers):
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