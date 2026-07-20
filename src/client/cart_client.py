from src.client.base_client import BaseClient
from src.models.carts.create_cart_request_model import CreateCartRequestModel

class CartClient(BaseClient):

    def get_all_carts(self, limit: int | None = None, skip: int | None = None):
        params = {
            "limit": limit,
            "skip": skip,
        }

        params = {k: v for k, v in params.items() if v is not None}

        return self.get("/carts", params=params)

    def get_cart(self, cart_id: int):
        return self.get(f"/carts/{cart_id}")

    def get_cart_by_user(self, user_id: int):
        return self.get(f"/carts/user/{user_id}")

    def add_cart(self, request: CreateCartRequestModel | dict):
        if isinstance(request, CreateCartRequestModel):
            request = request.model_dump()

        return self.post(
            "/carts/add",
            json=self._serialize_payload(request)
        )

