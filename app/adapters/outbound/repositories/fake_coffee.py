class FakeCoffeeRepository:
    async def search(self, filters):
        return [{
            "id": "coffee-001",
            "name": "Geisha Huila",
            "method": "V60",
            "profile": "frutal",
            "price_250g": 50000,
        }]

    async def create(self, product):
        return {
            "id": "coffee-001",
            "sku": product["sku"],
            "name": product["name"],
            "description": product.get("description"),
            "status": product.get("status", "ACTIVE"),
            "featured": product.get("featured", False),
        }
