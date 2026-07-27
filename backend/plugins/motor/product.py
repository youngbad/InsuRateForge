from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from decimal import Decimal
from typing import Any

from pydantic import BaseModel, Field, field_validator

from rateforge.domain.products.interfaces import ProductPlugin

from .rates import (
    BASE_RATE,
    COVER_FACTORS,
    MINIMUM_PREMIUM,
    POLICY_FEE,
    REGION_FACTORS,
    TAX_RATE,
    VEHICLE_TYPE_FACTORS,
    age_factor,
    claims_factor,
    mileage_factor,
)


class MotorRiskInput(BaseModel):
    driver_age: int = Field(ge=18, le=90)
    vehicle_value: float = Field(gt=1000)
    vehicle_type: str
    region: str
    annual_mileage: int = Field(gt=0, le=100000)
    cover_type: str
    claims_last_5_years: int = Field(ge=0, le=10)
    no_claims_years: int = Field(default=0, ge=0, le=15)
    loyalty_years: int = Field(default=0, ge=0, le=50)
    additional_drivers: int = Field(default=0, ge=0, le=10)
    start_date: datetime = Field(default_factory=lambda: datetime.now(UTC))

    @field_validator("vehicle_type")
    @classmethod
    def validate_vehicle_type(cls, value: str) -> str:
        normalized = value.strip().lower()
        if normalized not in VEHICLE_TYPE_FACTORS:
            raise ValueError(f"unsupported vehicle_type '{value}'")
        return normalized

    @field_validator("region")
    @classmethod
    def validate_region(cls, value: str) -> str:
        normalized = value.strip().lower()
        if normalized not in REGION_FACTORS:
            raise ValueError(f"unsupported region '{value}'")
        return normalized

    @field_validator("cover_type")
    @classmethod
    def validate_cover_type(cls, value: str) -> str:
        normalized = value.strip().lower()
        if normalized not in COVER_FACTORS:
            raise ValueError(f"unsupported cover_type '{value}'")
        return normalized


@dataclass(slots=True)
class MotorInsuranceProduct(ProductPlugin):
    version: str = "2024.1"
    config: dict[str, Any] = field(default_factory=dict)

    def validate(self, payload: dict[str, Any]) -> dict[str, Any]:
        return MotorRiskInput.model_validate(payload).model_dump(mode="json")

    def calculate(self, payload: dict[str, Any]) -> dict[str, Any]:
        risk = MotorRiskInput.model_validate(payload)
        base_value = Decimal(str(risk.vehicle_value)) * Decimal(str(BASE_RATE))
        factor = Decimal(str(age_factor(risk.driver_age)))
        factor *= Decimal(str(VEHICLE_TYPE_FACTORS[risk.vehicle_type]))
        factor *= Decimal(str(REGION_FACTORS[risk.region]))
        factor *= Decimal(str(COVER_FACTORS[risk.cover_type]))
        factor *= Decimal(str(claims_factor(risk.claims_last_5_years)))
        factor *= Decimal(str(mileage_factor(risk.annual_mileage)))
        factor *= Decimal(str(1 + (risk.additional_drivers * 0.03)))
        base_premium = max(Decimal(str(MINIMUM_PREMIUM)), (base_value * factor).quantize(Decimal("0.01")))
        return {
            "base_premium": float(base_premium),
            "policy_fee": self.config.get("policy_fee", POLICY_FEE),
            "tax_rate": self.config.get("tax_rate", TAX_RATE),
            "recommended_discounts": [
                {"name": "no_claims", "rate": min(risk.no_claims_years * 0.03, 0.25)},
                {"name": "loyalty", "rate": min(risk.loyalty_years * 0.01, 0.1)},
            ],
            "metadata": {
                "age_factor": age_factor(risk.driver_age),
                "vehicle_factor": VEHICLE_TYPE_FACTORS[risk.vehicle_type],
                "region_factor": REGION_FACTORS[risk.region],
                "cover_factor": COVER_FACTORS[risk.cover_type],
                "claims_factor": claims_factor(risk.claims_last_5_years),
                "mileage_factor": mileage_factor(risk.annual_mileage),
            },
        }

    def renew(self, existing_quote: dict[str, Any]) -> dict[str, Any]:
        payload = existing_quote["input_payload"].copy()
        payload["no_claims_years"] = int(payload.get("no_claims_years", 0)) + 1
        payload["vehicle_value"] = round(float(payload["vehicle_value"]) * 0.97, 2)
        payload["start_date"] = datetime.now(UTC).isoformat()
        return payload

    def endorsement(self, existing_quote: dict[str, Any], changes: dict[str, Any]) -> dict[str, Any]:
        payload = existing_quote["input_payload"].copy()
        payload.update(changes)
        return self.validate(payload)

    def summary(self, payload: dict[str, Any]) -> dict[str, Any]:
        risk = MotorRiskInput.model_validate(payload)
        return {
            "product": "motor",
            "version": self.version,
            "headline": f"{risk.cover_type.replace('_', ' ').title()} cover for a {risk.vehicle_type}",
            "risk_profile": {
                "driver_age": risk.driver_age,
                "claims_last_5_years": risk.claims_last_5_years,
                "region": risk.region,
            },
        }
