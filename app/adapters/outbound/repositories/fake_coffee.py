class FakeCoffeeRepository:
    async def search(self, filters):
        return [{
            "id": "coffee-001",
            "name": "Geisha Huila",
            "method": "V60",
            "profile": "frutal",
            "price_250g": 50000,
        }]
