from http.server import BaseHTTPRequestHandler
import json
import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from data import get_all_categories
except ImportError as e:
    print(f"Import error: {e}")
    # Fallback data structure
    def get_all_categories():
        return []

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            categories = get_all_categories()
            
            response_data = {
                'categories': categories
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
            print(f"Error in categories endpoint: {e}")
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            error_response = {
                'error': 'Internal server error',
                'message': str(e),
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
