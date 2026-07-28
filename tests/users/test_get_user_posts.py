import pytest

from src.models.posts.posts_response_model import PostsResponseModel
from src.models.error_response_model import ErrorResponseModel
from src.constants import INVALID_USER_ID_MESSAGE, USER_NOT_FOUND_MESSAGE


@pytest.mark.smoke
def test_get_user_posts(users_client):
    response = users_client.get_user_posts(1)

    assert response.status_code == 200

    posts = PostsResponseModel.model_validate(response.json())

    assert posts.total > 0
    assert len(posts.posts) == posts.total

    assert all(post.userId == 1 for post in posts.posts)

@pytest.mark.negative
def test_get_user_posts_invalid_user_id(users_client):
    response = users_client.get_user_posts(999999)

    assert response.status_code == 404
    # assert response.json() == {
    #     "message": "User with id '999999' not found"
    # }
    error = ErrorResponseModel.model_validate(response.json())

    assert error.message == USER_NOT_FOUND_MESSAGE.format("999999")

@pytest.mark.negative
def test_get_user_posts_with_invalid_user_id_returns_bad_request(users_client):
    response = users_client.get_user_posts("abc")

    assert response.status_code == 400

    error = ErrorResponseModel.model_validate(response.json())

    assert error.message == INVALID_USER_ID_MESSAGE.format("abc")