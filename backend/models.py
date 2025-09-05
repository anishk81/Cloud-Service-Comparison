from pydantic import BaseModel
from typing import List, Optional
from enum import Enum

class ServiceCategory(str, Enum):
    COMPUTE = "Compute"
    STORAGE = "Storage"
    DATABASE = "Database"
    NETWORKING = "Networking"
    SECURITY = "Security"
    ANALYTICS = "Analytics"
    MACHINE_LEARNING = "Machine Learning"
    CONTAINERS = "Containers"
    SERVERLESS = "Serverless"
    DEVELOPER_TOOLS = "Developer Tools"
    MANAGEMENT = "Management & Governance"
    IOT = "Internet of Things"

class PricingModel(str, Enum):
    ON_DEMAND = "On-Demand"
    RESERVED = "Reserved Instances"
    SPOT = "Spot Pricing"
    FREE_TIER = "Free Tier"
    PAY_PER_USE = "Pay-per-use"

class AWSService(BaseModel):
    id: str
    name: str
    description: str
    category: ServiceCategory
    key_features: List[str]
    pricing_notes: str
    pricing_models: List[PricingModel]
    use_cases: List[str]
    limitations: Optional[List[str]] = []
    free_tier_available: bool = False
    region_availability: str = "Most AWS regions"
    documentation_url: Optional[str] = None

class ServiceComparison(BaseModel):
    services: List[AWSService]
    comparison_criteria: List[str]

class CategoryResponse(BaseModel):
    categories: List[ServiceCategory]

class ServicesResponse(BaseModel):
    services: List[AWSService]
    total_count: int
    categories: List[ServiceCategory]
