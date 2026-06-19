from src.client.base_client import BaseClient


class AuthClient(BaseClient):

    def login(self, username: str, password: str):
        return self.post(
            "/auth/login",
            json={"username": username, "password": password},
        )

    def get_current_user(self, token: str):
        return self.session.get(
            f"{self.base_url}/auth/me",
            headers={"Authorization": f"Bearer {token}"},
        )