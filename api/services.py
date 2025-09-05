from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

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
    
    return {
        "services": services,
        "total_count": len(services),
        "categories": get_all_categories()
    }

# For Vercel serverless function
handler = app
