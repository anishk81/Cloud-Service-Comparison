from http.server import BaseHTTPRequestHandler
import json
import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from data import get_all_services
except ImportError as e:
    print(f"Import error: {e}")
    # Fallback data structure
    def get_all_services():
        return []

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            services = get_all_services()
            
            response_data = {
                'status': 'healthy',
                'services_count': len(services)
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
            print(f"Error in health endpoint: {e}")
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            error_response = {
                'error': 'Internal server error',
                'message': str(e),
                'status': 'unhealthy',
                'services_count': 0
            }
            self.wfile.write(json.dumps(error_response).encode())
    
    def do_OPTIONS(self):
        # Handle CORS preflight requests
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
