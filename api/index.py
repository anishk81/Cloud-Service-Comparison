from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from models import AWSService, ServiceCategory, ServicesResponse
from data import get_all_services, get_service_by_id, get_services_by_category, get_all_categories

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
@app.get("/api")
async def root():
    return {
        "message": "AWS Service Comparison API",
        "version": "1.0.0",
        "endpoints": {
            "/api/services": "Get all AWS services",
            "/api/categories": "Get all service categories",
            "/api/health": "Health check"
        }
    }

@app.get("/api/services")
async def get_services(
    category: Optional[str] = Query(None),
    free_tier: Optional[bool] = Query(None),
    search: Optional[str] = Query(None)
):
    services = get_all_services()
    
    if category:
        try:
            category_enum = ServiceCategory(category)
            services = [s for s in services if s.category == category_enum]
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid category: {category}")
    
    if free_tier is not None:
        services = [s for s in services if s.free_tier_available == free_tier]
    
    if search:
        search_lower = search.lower()
        services = [
            s for s in services 
            if search_lower in s.name.lower() or search_lower in s.description.lower()
        ]
    
    return {
        "services": services,
        "total_count": len(services),
        "categories": get_all_categories()
    }

@app.get("/api/categories")
async def get_categories():
    return {"categories": get_all_categories()}

@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "services_count": len(get_all_services())}

@app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def catch_all(request: Request, path: str):
    return await root()

# Export handler for Vercel
handler = app
