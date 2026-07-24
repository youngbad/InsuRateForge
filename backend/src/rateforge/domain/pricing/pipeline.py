from __future__ import annotations

from dataclasses import asdict
from typing import Any

from rateforge.domain.pricing.entities import PricingResult
from rateforge.domain.pricing.interfaces import PipelineStage, PricingContext


def _normalize_value(value: Any) -> Any:
    if isinstance(value, dict):
        return {key: _normalize_value(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_normalize_value(item) for item in value]
    if isinstance(value, str):
        stripped = value.strip()
        if stripped.replace(".", "", 1).isdigit():
            return float(stripped) if "." in stripped else int(stripped)
        return stripped
    return value


class ValidationStage(PipelineStage):
    async def execute(self, context: PricingContext) -> PricingContext:
        context.validated_payload = context.plugin.validate(context.payload)
        return context


class NormalizeStage(PipelineStage):
    async def execute(self, context: PricingContext) -> PricingContext:
        context.normalized_payload = _normalize_value(context.validated_payload)
        return context


class RateStage(PipelineStage):
    async def execute(self, context: PricingContext) -> PricingContext:
        context.calculation = context.plugin.calculate(context.normalized_payload)
        context.base_premium = float(context.calculation["base_premium"])
        context.metadata.update(context.calculation.get("metadata", {}))
        return context


class DiscountStage(PipelineStage):
    async def execute(self, context: PricingContext) -> PricingContext:
        raw_discounts = context.calculation.get("recommended_discounts", [])
        context.discounts = [
            {
                "name": item["name"],
                "rate": float(item["rate"]),
                "amount": round(context.base_premium * float(item["rate"]), 2),
            }
            for item in raw_discounts
            if float(item["rate"]) > 0
        ]
        return context


class TaxStage(PipelineStage):
    async def execute(self, context: PricingContext) -> PricingContext:
        taxable_amount = context.base_premium - sum(item["amount"] for item in context.discounts)
        tax_rate = float(context.calculation.get("tax_rate", 0.0))
        tax_amount = round(taxable_amount * tax_rate, 2)
        context.taxes = [{"name": "insurance_tax", "rate": tax_rate, "amount": tax_amount}]
        return context


class FeeStage(PipelineStage):
    async def execute(self, context: PricingContext) -> PricingContext:
        fee_amount = round(float(context.calculation.get("policy_fee", 0.0)), 2)
        if fee_amount > 0:
            context.fees = [{"name": "policy_fee", "amount": fee_amount}]
        return context


class OutputStage(PipelineStage):
    async def execute(self, context: PricingContext) -> PricingContext:
        return context


class PricingPipeline:
    def __init__(self) -> None:
        self.stages: list[PipelineStage] = [
            ValidationStage(),
            NormalizeStage(),
            RateStage(),
            DiscountStage(),
            TaxStage(),
            FeeStage(),
            OutputStage(),
        ]

    async def run(self, context: PricingContext) -> PricingResult:
        for stage in self.stages:
            context = await stage.execute(context)
        discounts_total = round(sum(item["amount"] for item in context.discounts), 2)
        taxes_total = round(sum(item["amount"] for item in context.taxes), 2)
        fees_total = round(sum(item["amount"] for item in context.fees), 2)
        total_premium = round(context.base_premium - discounts_total + taxes_total + fees_total, 2)
        breakdown = {
            "discounts": context.discounts,
            "taxes": context.taxes,
            "fees": context.fees,
            "metadata": context.metadata,
            "calculation": context.calculation,
            "context": asdict(context),
        }
        return PricingResult(
            product_slug=context.product_slug,
            product_version=context.product_version,
            currency="USD",
            base_premium=round(context.base_premium, 2),
            discounts_total=discounts_total,
            taxes_total=taxes_total,
            fees_total=fees_total,
            total_premium=total_premium,
            breakdown=breakdown,
            normalized_payload=context.normalized_payload,
            summary=context.plugin.summary(context.normalized_payload),
        )
