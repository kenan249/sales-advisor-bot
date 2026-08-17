import asyncio
from uuid import uuid4

from app.adapters.outbound.repositories.coffee_repository import CoffeeRepository
from app.shared.config import settings
from app.shared import database


async def main():
    if not settings.database_url:
        raise RuntimeError("DATABASE_URL no está configurada en el archivo .env")

    print("DATABASE_URL configurada: sí")
    session_factory = database.create_session_factory(settings.database_url)
    coffee_repository = CoffeeRepository(session_factory)

    product = await coffee_repository.create({
        "sku": f"CHIROSO-{uuid4().hex[:8].upper()}",
        "name": "Chiroso Caldas",
        "description": "Notas citricas y avinadas",
        "featured": True,
    })
    print(f"Producto creado: {product}")


if __name__ == "__main__":
    asyncio.run(main())
