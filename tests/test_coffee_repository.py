from uuid import uuid4

import pytest

from app.adapters.outbound.repositories.coffee_repository import CoffeeRepository


class FakeResult:
    def __init__(self, row):
        self._row = row

    def mappings(self):
        return self

    def one(self):
        return self._row


class FakeTransaction:
    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        return None


class FakeSession:
    def __init__(self, row):
        self._row = row

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        return None

    def begin(self):
        return FakeTransaction()

    async def execute(self, statement):
        return FakeResult(self._row)


@pytest.mark.asyncio
async def test_create_inserts_and_returns_a_product():
    product_id = uuid4()
    row = {
        "id": product_id,
        "sku": "GEISHA-250",
        "name": "Geisha Huila",
        "description": "Notas florales",
        "status": "ACTIVE",
        "featured": True,
    }
    repository = CoffeeRepository(lambda: FakeSession(row))

    product = await repository.create({
        "sku": "GEISHA-250",
        "name": "Geisha Huila",
        "description": "Notas florales",
        "featured": True,
    })

    assert product == {**row, "id": str(product_id)}
