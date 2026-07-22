# DELETE
import pytest

from src.models.users.user_model import UserModel

@pytest.mark.smoke
def test_delete_user(users_client):
    response = users_client.delete_user(1)

    assert response.status_code == 200

    deleted = UserModel.model_validate(response.json())

    assert deleted.id == 1
    assert deleted.isDeleted is True
    assert deleted.deletedOn is not None

