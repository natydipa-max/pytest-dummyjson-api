from src.client.base_client import BaseClient
from src.models.product_request_model import ProductRequestModel


class ProductClient(BaseClient):

    def get_all_products(self):
        return self.get("/products")

    def get_product(self, product_id: int):
        return self.get(f"/products/{product_id}")

    def create_product(self, product: ProductRequestModel):
        return self.post(
            "/products/add",
            json=product.model_dump(),
        )

    def update_product(self, product_id: int, product: ProductRequestModel):
        return self.put(
            f"/products/{product_id}",
            json=product.model_dump(),
        )

    def delete_product(self, product_id: int):
        return self.delete(f"/products/{product_id}")