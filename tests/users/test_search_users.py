import pytest
from src.models.users.users_response_model import UsersResponseModel

@pytest.mark.smoke
def test_search_users(users_client):
    response = users_client.search_users("Noah")

    assert response.status_code == 200

    users = UsersResponseModel.model_validate(response.json())

    assert users.total >= 1
    assert any(u.firstName == "Noah" for u in users.users)


@pytest.mark.parametrize(
    "query, field, expected",
    [
        ("Noah", "firstName", "Noah"),
        ("Hernandez", "lastName", "Hernandez"),
        ("noahh", "username", "noahh"),
    ],
)
def test_search_users_positive(users_client, query, field, expected):
    response = users_client.search_users(query)

    assert response.status_code == 200

    users = UsersResponseModel.model_validate(response.json())

    assert len(users.users) > 0

    assert all(getattr(user, field) == expected for user in users.users)


@pytest.mark.parametrize(
    "query",
    [
        "XXX",
        "NonExistingUser",
        "@@@###",
    ],
)
def test_search_users_returns_empty_list_when_no_matches(users_client, query):
    response = users_client.search_users(query)

    assert response.status_code == 200

    users = UsersResponseModel.model_validate(response.json())

    assert users.total == 0
    assert users.limit == 0
    assert users.users == []