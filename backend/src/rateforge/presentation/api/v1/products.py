from __future__ import annotations

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from rateforge.application.products.commands import ProductService
from rateforge.application.products.dtos import ProductDTO, RegisterProductDTO
from rateforge.presentation.dependencies import (
    get_product_service,
    get_session,
    require_roles,
    write_audit_log,
)

router = APIRouter()


@router.get("/", response_model=list[ProductDTO])
async def list_products(product_service: ProductService = Depends(get_product_service)) -> list[ProductDTO]:
    return await product_service.list()


@router.post("/", response_model=ProductDTO, status_code=status.HTTP_201_CREATED)
async def register_product(
    command: RegisterProductDTO,
    product_service: ProductService = Depends(get_product_service),
    session: AsyncSession = Depends(get_session),
    _=Depends(require_roles("admin", "underwriter")),
) -> ProductDTO:
    product = await product_service.register(command)
    await write_audit_log(
        session,
        actor_user_id=None,
        action="product.registered",
        resource_type="product",
        resource_id=product.id,
        payload={"slug": product.slug, "version": product.version},
    )
    return product
