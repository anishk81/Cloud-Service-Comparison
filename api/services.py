from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import json
import sys
import os
from typing import Optional

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from models import ServiceCategory
    from data import get_all_services, get_all_categories
except ImportError as e:
    print(f"Import error: {e}")
    # Fallback data structure
    def get_all_services():
        return []
    def get_all_categories():
        return []

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            # Parse URL and query parameters
            parsed_url = urlparse(self.path)
            query_params = parse_qs(parsed_url.query)
            
            # Get services with optional filtering
            services = get_all_services()
            
            # Apply category filter
            category = query_params.get('category', [None])[0]
            if category:
                try:
                    category_enum = ServiceCategory(category)
                    services = [s for s in services if s.category == category_enum]
                except (ValueError, Exception):
                    pass  # Invalid category, ignore filter
            
            # Apply free tier filter
            free_tier_param = query_params.get('free_tier', [None])[0]
            if free_tier_param is not None:
                free_tier = free_tier_param.lower() == 'true'
                services = [s for s in services if s.free_tier_available == free_tier]
            
            # Apply search filter
            search = query_params.get('search', [None])[0]
            if search:
                search_lower = search.lower()
                services = [
                    s for s in services 
                    if search_lower in s.name.lower() or search_lower in s.description.lower()
                ]
            
            # Convert services to dict format
            services_data = []
            for service in services:
                try:
                    service_dict = {
                        'id': service.id,
                        'name': service.name,
                        'category': service.category.value if hasattr(service.category, 'value') else str(service.category),
                        'description': service.description,
                        'key_features': service.key_features,
                        'pricing_models': service.pricing_models,
                        'use_cases': service.use_cases,
                        'limitations': service.limitations,
                        'free_tier_available': service.free_tier_available,
                        'region_availability': service.region_availability
                    }
                    services_data.append(service_dict)
                except Exception as e:
                    print(f"Error serializing service: {e}")
                    continue
            
            response_data = {
                'services': services_data,
                'total_count': len(services_data),
                'categories': get_all_categories()
            }
            
            # Set CORS headers
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            self.end_headers()
            
            # Send JSON response
            self.wfile.write(json.dumps(response_data).encode())
            
        except Exception as e:
            print(f"Error in services endpoint: {e}")
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            error_response = {
                'error': 'Internal server error',
                'message': str(e),
                'services': [],
                'total_count': 0,
                'categories': []
            }
            self.wfile.write(json.dumps(error_response).encode())
    
    def do_OPTIONS(self):
        # Handle CORS preflight requests
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
