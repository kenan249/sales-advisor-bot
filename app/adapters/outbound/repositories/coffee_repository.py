from decimal import Decimal
from typing import Any

from sqlalchemy import (
    Boolean,
    Column,
    Integer,
    MetaData,
    Numeric,
    String,
    Table,
    and_,
    func,
    insert,
    select,
    text,
)
from sqlalchemy.dialects.postgresql import ENUM, UUID
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker


metadata = MetaData()
product_status = ENUM(
    "ACTIVE",
    "INACTIVE",
    "OUT_OF_STOCK",
    name="product_status",
    create_type=False,
)

products = Table(
    "products",
    metadata,
    Column(
        "id",
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("uuid_generate_v4()"),
    ),
    Column("sku", String),
    Column("name", String),
    Column("description", String),
    Column("status", product_status),
    Column("featured", Boolean),
)
product_presentations = Table(
    "product_presentations",
    metadata,
    Column("id", UUID(as_uuid=True), primary_key=True),
    Column("product_id", UUID(as_uuid=True)),
    Column("weight_grams", Integer),
    Column("price", Numeric),
    Column("currency", String),
    Column("active", Boolean),
)
inventory = Table(
    "inventory",
    metadata,
    Column("product_presentation_id", UUID(as_uuid=True), primary_key=True),
    Column("quantity_available", Integer),
    Column("quantity_reserved", Integer),
)
preparation_methods = Table(
    "preparation_methods",
    metadata,
    Column("id", UUID(as_uuid=True), primary_key=True),
    Column("name", String),
)
product_methods = Table(
    "product_methods",
    metadata,
    Column("product_id", UUID(as_uuid=True), primary_key=True),
    Column("method_id", UUID(as_uuid=True), primary_key=True),
)


class CoffeeRepository:
    """Consulta los productos de café disponibles."""

    def __init__(self, session_factory: async_sessionmaker[AsyncSession]) -> None:
        self._session_factory = session_factory

    async def search(self, filters: dict) -> list[dict]:
        async with self._session_factory() as session:
            result = await session.execute(self._build_query(filters))
            return [self._to_dict(row) for row in result.mappings().all()]

    async def create(self, product: dict) -> dict:
        """Inserta un producto de café y retorna sus datos principales."""
        statement = (
            insert(products)
            .values(
                sku=product["sku"],
                name=product["name"],
                description=product.get("description"),
                status=product.get("status", "ACTIVE"),
                featured=product.get("featured", False),
            )
            .returning(
                products.c.id,
                products.c.sku,
                products.c.name,
                products.c.description,
                products.c.status,
                products.c.featured,
            )
        )
        async with self._session_factory() as session:
            async with session.begin():
                result = await session.execute(statement)
                row = result.mappings().one()
        return {
            "id": str(row["id"]),
            "sku": row["sku"],
            "name": row["name"],
            "description": row["description"],
            "status": row["status"],
            "featured": row["featured"],
        }

    @staticmethod
    def _build_query(filters: dict):
        limit = min(max(int(filters.get("limit", 10)), 1), 50)
        query = (
            select(
                products.c.id.label("product_id"),
                products.c.sku,
                products.c.name,
                products.c.description,
                product_presentations.c.id.label("presentation_id"),
                product_presentations.c.weight_grams,
                product_presentations.c.price,
                product_presentations.c.currency,
                preparation_methods.c.name.label("method"),
            )
            .select_from(
                products.join(
                    product_presentations,
                    products.c.id == product_presentations.c.product_id,
                )
                .join(
                    inventory,
                    inventory.c.product_presentation_id == product_presentations.c.id,
                )
                .outerjoin(product_methods, product_methods.c.product_id == products.c.id)
                .outerjoin(
                    preparation_methods,
                    preparation_methods.c.id == product_methods.c.method_id,
                )
            )
            .where(
                and_(
                    products.c.status == "ACTIVE",
                    product_presentations.c.active.is_(True),
                    inventory.c.quantity_available > inventory.c.quantity_reserved,
                )
            )
            .order_by(products.c.featured.desc(), products.c.name, product_presentations.c.weight_grams)
            .limit(limit)
        )

        if method := filters.get("method"):
            query = query.where(func.lower(preparation_methods.c.name) == str(method).lower())
        if name := filters.get("name") or filters.get("query"):
            query = query.where(products.c.name.ilike(f"%{name}%"))
        if weight := filters.get("weight_grams"):
            query = query.where(product_presentations.c.weight_grams == int(weight))
        return query

    @staticmethod
    def _to_dict(row: Any) -> dict:
        return {
            "id": str(row["product_id"]),
            "presentation_id": str(row["presentation_id"]),
            "sku": row["sku"],
            "name": row["name"],
            "description": row["description"],
            "method": row["method"],
            "weight_grams": row["weight_grams"],
            "price": float(row["price"]) if isinstance(row["price"], Decimal) else row["price"],
            "currency": row["currency"],
        }
