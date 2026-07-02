from src.client.base_client import BaseClient
from src.models.users_response_model import UsersResponseModel


class UserClient(BaseClient):

    def get_all_users(self):
        return self.get("/users")

    def get_user(self, user_id: int):
        return self.get(f"/users/{user_id}")

    def search_users(self, query: str) -> UsersResponseModel:
        return self.get("/users/search", params={"q": query})