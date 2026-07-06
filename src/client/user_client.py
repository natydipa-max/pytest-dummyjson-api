from src.client.base_client import BaseClient
from src.models.users.user_request_model import UserRequestModel


class UserClient(BaseClient):

    def get_all_users(self):
        return self.get("/users")

    def get_user(self, user_id: int):
        return self.get(f"/users/{user_id}")

    def search_users(self, query: str):
        return self.get("/users/search", params={"q": query})

    def create_user(self, payload: UserRequestModel | dict):
        if isinstance(payload, UserRequestModel):
            payload = payload.model_dump()

        return self.post(
            "/users/add",
            json=self._serialize_payload(payload)
        )