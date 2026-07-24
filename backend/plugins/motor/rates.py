BASE_RATE = 0.018
MINIMUM_PREMIUM = 250.0
TAX_RATE = 0.15
POLICY_FEE = 35.0

VEHICLE_TYPE_FACTORS = {
    "sedan": 1.0,
    "suv": 1.15,
    "truck": 1.25,
    "electric": 0.92,
    "sports": 1.45,
}

REGION_FACTORS = {
    "urban": 1.12,
    "suburban": 1.0,
    "rural": 0.91,
}

COVER_FACTORS = {
    "third_party": 0.72,
    "third_party_fire_theft": 0.86,
    "comprehensive": 1.0,
}

def age_factor(age: int) -> float:
    if age < 25:
        return 1.35
    if age < 35:
        return 1.1
    if age < 60:
        return 1.0
    return 1.08

def claims_factor(claims_last_5_years: int) -> float:
    return 1.0 + (claims_last_5_years * 0.12)

def mileage_factor(annual_mileage: int) -> float:
    if annual_mileage <= 10000:
        return 0.95
    if annual_mileage <= 20000:
        return 1.0
    return 1.12
