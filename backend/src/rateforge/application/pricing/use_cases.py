from __future__ import annotations

from importlib import import_module
from statistics import mean
from typing import Any

from rateforge.domain.pricing.entities import PricingResult
from rateforge.domain.pricing.interfaces import PricingContext
from rateforge.domain.pricing.pipeline import PricingPipeline
from rateforge.infrastructure.database.repositories.products import SQLAlchemyProductRepository


class PricingError(ValueError):
    pass


class ProductPluginRegistry:
    def __init__(self) -> None:
        self._instances: dict[tuple[str, str], object] = {}

    def load(self, *, slug: str, version: str, plugin_path: str, config: dict[str, Any]) -> object:
        key = (slug, version)
        if key in self._instances:
            return self._instances[key]
        module_name, class_name = plugin_path.split(":", maxsplit=1)
        module = import_module(module_name)
        plugin_cls = getattr(module, class_name)
        plugin = plugin_cls(version=version, config=config)
        self._instances[key] = plugin
        return plugin


class PricingEngineService:
    def __init__(
        self,
        product_repo: SQLAlchemyProductRepository,
        plugin_registry: ProductPluginRegistry | None = None,
    ) -> None:
        self.product_repo = product_repo
        self.plugin_registry = plugin_registry or ProductPluginRegistry()
        self.pipeline = PricingPipeline()

    async def rate_quote(
        self,
        *,
        product_slug: str,
        payload: dict[str, object],
        product_version: str | None = None,
    ) -> PricingResult:
        product = await self.product_repo.get_by_slug(product_slug, product_version)
        if product is None:
            raise PricingError(f"Product '{product_slug}' not found")
        plugin = self.plugin_registry.load(
            slug=product.slug,
            version=product.version,
            plugin_path=product.plugin_path,
            config=product.config,
        )
        context = PricingContext(
            product_slug=product.slug,
            product_version=product.version,
            plugin=plugin,  # type: ignore[arg-type]
            payload=payload,
        )
        return await self.pipeline.run(context)

    async def run_portfolio(self, product_slug: str, payloads: list[dict[str, object]]) -> dict[str, object]:
        if not payloads:
            raise PricingError("At least one payload is required")
        results = [await self.rate_quote(product_slug=product_slug, payload=payload) for payload in payloads]
        totals = [result.total_premium for result in results]
        return {
            "product_slug": product_slug,
            "count": len(results),
            "average_premium": round(mean(totals), 2),
            "min_premium": round(min(totals), 2),
            "max_premium": round(max(totals), 2),
            "results": [result.__dict__ for result in results],
        }
