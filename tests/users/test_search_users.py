import pytest
from src.models.users_response_model import UsersResponseModel

@pytest.mark.smoke
def test_search_users_by_first_name(users_client):
    response = users_client.search_users("Noah")

    assert response.status_code == 200

    users = UsersResponseModel.model_validate(response.json())

    assert all(user.firstName == "Noah" for user in users.users)


@pytest.mark.parametrize("query, expected_min_results", [
    ("Noah", 1),
    ("noah", 1),
    ("No", 1),
])
def test_search_users_positive(users_client, query, expected_min_results):
    response = users_client.search_users(query)

    assert response.status_code == 200

    users = UsersResponseModel.model_validate(response.json())

    assert len(users.users) >= expected_min_results

    assert all(query.lower() in user.firstName.lower() for user in users.users)


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

    assert len(users.users) == 0