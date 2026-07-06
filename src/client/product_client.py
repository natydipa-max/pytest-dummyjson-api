from src.client.base_client import BaseClient
from src.models.products.product_request_model import ProductRequestModel


class ProductClient(BaseClient):

    def get_all_products(self):
        return self.get("/products")

    def get_product(self, product_id: int):
        return self.get(f"/products/{product_id}")

    def create_product(self, payload: ProductRequestModel | dict):
        if isinstance(payload, ProductRequestModel):
            payload = payload.model_dump()

        return self.post(
            "/products/add",
            json=self._serialize_payload(payload)
        )

    def update_product(self, product_id: int, product: ProductRequestModel):
        return self.put(
            f"/products/{product_id}",
            json=product.model_dump(),
        )

    def delete_product(self, product_id: int):
        return self.delete(f"/products/{product_id}")