from src.client.base_client import BaseClient
#from src.models.user_request_model import UserRequestModel


class UserClient(BaseClient):

    def get_all_users(self):
        return self.get("/users")

    def get_user(self, user_id: int):
        return self.get(f"/users/{user_id}")

    