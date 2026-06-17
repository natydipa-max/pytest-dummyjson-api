import pytest

from src.client.product_client import ProductClient


@pytest.fixture(scope="session")
def products_client():
    return ProductClient()