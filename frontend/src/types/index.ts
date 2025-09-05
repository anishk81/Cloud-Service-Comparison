export interface AWSService {
  id: string;
  name: string;
  description: string;
  category: ServiceCategory;
  key_features: string[];
  pricing_notes: string;
  pricing_models: PricingModel[];
  use_cases: string[];
  limitations: string[];
  free_tier_available: boolean;
  region_availability: string;
  documentation_url?: string;
}

export interface ServicesResponse {
  services: AWSService[];
  total_count: number;
  categories: ServiceCategory[];
}

export interface ComparisonResponse {
  services: AWSService[];
  comparison_criteria: string[];
  comparison_count: number;
}

export enum ServiceCategory {
  COMPUTE = "Compute",
  STORAGE = "Storage",
  DATABASE = "Database",
  NETWORKING = "Networking",
  SECURITY = "Security",
  ANALYTICS = "Analytics",
  MACHINE_LEARNING = "Machine Learning",
  CONTAINERS = "Containers",
  SERVERLESS = "Serverless",
  DEVELOPER_TOOLS = "Developer Tools",
  MANAGEMENT = "Management & Governance",
  IOT = "Internet of Things",
}

export enum PricingModel {
  ON_DEMAND = "On-Demand",
  RESERVED = "Reserved Instances",
  SPOT = "Spot Pricing",
  FREE_TIER = "Free Tier",
  PAY_PER_USE = "Pay-per-use",
}
