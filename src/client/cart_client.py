from src.client.base_client import BaseClient


class CartClient(BaseClient):

    def get_all_carts(self):
        return self.get("/carts")

    def get_cart(self, cart_id: int):
        return self.get(f"/carts/{cart_id}")

    def get_cart_by_user(self, user_id: int):
        return self.get(f"/carts/user/{user_id}")

