from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from models import AWSService, ServiceCategory, ServicesResponse, CategoryResponse
from data import get_all_services, get_service_by_id, get_services_by_category, get_all_categories

app = FastAPI(
    title="AWS Service Comparison API",
    description="API for comparing AWS services with detailed information about categories, features, and pricing",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000", 
        "http://localhost:3001",  # React dev server
    ],
    allow_origin_regex=r"https://.*\.vercel\.app",  # All Vercel deployments
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {
        "message": "AWS Service Comparison API",
        "version": "1.0.0",
        "endpoints": {
            "/api/services": "Get all AWS services",
            "/api/services/{service_id}": "Get specific service details",
            "/api/categories": "Get all service categories",
            "/api/services/category/{category}": "Get services by category"
        }
    }

@app.get("/api/services", response_model=ServicesResponse)
async def get_services(
    category: Optional[str] = Query(None, description="Filter by category"),
    free_tier: Optional[bool] = Query(None, description="Filter by free tier availability"),
    search: Optional[str] = Query(None, description="Search in service names and descriptions")
):
    """Get all AWS services with optional filtering"""
    services = get_all_services()
    
    # Apply category filter
    if category:
        try:
            category_enum = ServiceCategory(category)
            services = [s for s in services if s.category == category_enum]
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid category: {category}")
    
    # Apply free tier filter
    if free_tier is not None:
        services = [s for s in services if s.free_tier_available == free_tier]
    
    # Apply search filter
    if search:
        search_lower = search.lower()
        services = [
            s for s in services 
            if search_lower in s.name.lower() or search_lower in s.description.lower()
        ]
    
    return ServicesResponse(
        services=services,
        total_count=len(services),
        categories=get_all_categories()
    )

@app.get("/api/services/{service_id}", response_model=AWSService)
async def get_service(service_id: str):
    """Get detailed information about a specific AWS service"""
    service = get_service_by_id(service_id)
    if not service:
        raise HTTPException(status_code=404, detail=f"Service not found: {service_id}")
    return service

@app.get("/api/categories", response_model=CategoryResponse)
async def get_categories():
    """Get all available service categories"""
    return CategoryResponse(categories=get_all_categories())

@app.get("/api/services/category/{category}", response_model=List[AWSService])
async def get_services_by_cat(category: str):
    """Get all services in a specific category"""
    try:
        category_enum = ServiceCategory(category)
        services = get_services_by_category(category_enum)
        return services
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Invalid category: {category}")

@app.get("/api/compare")
async def compare_services(service_ids: str = Query(..., description="Comma-separated service IDs")):
    """Compare multiple services side by side"""
    ids = [id.strip() for id in service_ids.split(",")]
    services = []
    
    for service_id in ids:
        service = get_service_by_id(service_id)
        if not service:
            raise HTTPException(status_code=404, detail=f"Service not found: {service_id}")
        services.append(service)
    
    if len(services) < 2:
        raise HTTPException(status_code=400, detail="At least 2 services are required for comparison")
    
    # Extract comparison criteria
    comparison_criteria = [
        "Category",
        "Key Features",
        "Pricing Models",
        "Use Cases",
        "Limitations",
        "Free Tier Available",
        "Region Availability"
    ]
    
    return {
        "services": services,
        "comparison_criteria": comparison_criteria,
        "comparison_count": len(services)
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "services_count": len(get_all_services())}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
