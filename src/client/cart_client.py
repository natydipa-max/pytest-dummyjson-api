from src.client.base_client import BaseClient


class CartClient(BaseClient):

    def get_all_carts(self):
        return self.get("/carts")

    def get_cart(self, cart_id: int):
        return self.get(f"/carts/{cart_id}")

