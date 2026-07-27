import pytest

@pytest.mark.boundary
def test_get_users_with_field_selection(users_client):
    response = users_client.get_all_users(
        select="firstName,age"
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data["users"]) > 0

    user = data["users"][0]

    assert set(user.keys()) == {"id", "firstName", "age"}