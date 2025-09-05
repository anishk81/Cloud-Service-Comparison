from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import json
import sys
import os
from typing import Optional

# Sample AWS services data
SAMPLE_SERVICES = [
    {
        'id': 'ec2',
        'name': 'Amazon EC2',
        'category': 'Compute',
        'description': 'Secure and resizable compute capacity in the cloud.',
        'key_features': ['Virtual servers', 'Multiple instance types', 'Auto Scaling', 'Elastic Load Balancing'],
        'pricing_models': ['On-Demand', 'Reserved Instances', 'Spot Instances'],
        'use_cases': ['Web hosting', 'Application hosting', 'Development environments'],
        'limitations': ['Requires OS management', 'Instance limits per region'],
        'free_tier_available': True,
        'region_availability': 'All AWS Regions'
    },
    {
        'id': 's3',
        'name': 'Amazon S3',
        'category': 'Storage',
        'description': 'Object storage service with industry-leading scalability.',
        'key_features': ['Unlimited storage', 'High durability', 'Web interface', 'REST API'],
        'pricing_models': ['Pay-as-you-go', 'Storage classes'],
        'use_cases': ['Backup and restore', 'Data archiving', 'Static website hosting'],
        'limitations': ['Regional service', 'Eventual consistency'],
        'free_tier_available': True,
        'region_availability': 'All AWS Regions'
    },
    {
        'id': 'lambda',
        'name': 'AWS Lambda',
        'category': 'Compute',
        'description': 'Run code without thinking about servers.',
        'key_features': ['Serverless', 'Event-driven', 'Auto scaling', 'Multiple runtimes'],
        'pricing_models': ['Pay per request', 'Pay per duration'],
        'use_cases': ['API backends', 'Data processing', 'Real-time file processing'],
        'limitations': ['15-minute execution limit', 'Cold start latency'],
        'free_tier_available': True,
        'region_availability': 'Most AWS Regions'
    },
    {
        'id': 'rds',
        'name': 'Amazon RDS',
        'category': 'Database',
        'description': 'Managed relational database service.',
        'key_features': ['Automated backups', 'Multi-AZ deployment', 'Read replicas', 'Multiple engines'],
        'pricing_models': ['On-Demand', 'Reserved Instances'],
        'use_cases': ['Web applications', 'Online transaction processing', 'Data warehousing'],
        'limitations': ['No shell access', 'Limited customization'],
        'free_tier_available': True,
        'region_availability': 'Most AWS Regions'
    },
    {
        'id': 'cloudfront',
        'name': 'Amazon CloudFront',
        'category': 'Networking',
        'description': 'Global content delivery network (CDN) service.',
        'key_features': ['Global edge locations', 'DDoS protection', 'SSL/TLS', 'Real-time metrics'],
        'pricing_models': ['Pay-as-you-go', 'Savings bundles'],
        'use_cases': ['Website acceleration', 'Video streaming', 'API acceleration'],
        'limitations': ['Cache invalidation costs', 'Geographic restrictions'],
        'free_tier_available': True,
        'region_availability': 'Global'
    },
    {
        'id': 'sns',
        'name': 'Amazon SNS',
        'category': 'Messaging',
        'description': 'Fully managed messaging service for both application-to-application and application-to-person communication.',
        'key_features': ['Topic-based pub/sub', 'SMS and email', 'Mobile push', 'Message filtering'],
        'pricing_models': ['Pay per message', 'No upfront costs'],
        'use_cases': ['Mobile app notifications', 'System alerts', 'Email campaigns'],
        'limitations': ['Message size limits', 'Regional service'],
        'free_tier_available': True,
        'region_availability': 'Most AWS Regions'
    },
    {
        'id': 'dynamodb',
        'name': 'Amazon DynamoDB',
        'category': 'Database',
        'description': 'Fast and flexible NoSQL database service.',
        'key_features': ['Serverless', 'Auto scaling', 'Built-in security', 'Global tables'],
        'pricing_models': ['On-demand', 'Provisioned capacity'],
        'use_cases': ['Mobile backends', 'Web applications', 'Gaming', 'IoT'],
        'limitations': ['Query limitations', 'Item size limits'],
        'free_tier_available': True,
        'region_availability': 'Most AWS Regions'
    },
    {
        'id': 'sagemaker',
        'name': 'Amazon SageMaker',
        'category': 'Machine Learning',
        'description': 'Fully managed service to build, train, and deploy machine learning models.',
        'key_features': ['Built-in algorithms', 'Jupyter notebooks', 'Model training', 'Auto scaling'],
        'pricing_models': ['Pay for compute time', 'Instance-based'],
        'use_cases': ['Predictive analytics', 'Computer vision', 'Natural language processing'],
        'limitations': ['Learning curve', 'Cost optimization needed'],
        'free_tier_available': False,
        'region_availability': 'Selected AWS Regions'
    }
]

CATEGORIES = ['Compute', 'Storage', 'Database', 'Networking', 'Messaging', 'Machine Learning', 'Analytics', 'Security', 'Developer Tools']

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            # Parse URL and query parameters
            parsed_url = urlparse(self.path)
            query_params = parse_qs(parsed_url.query)
            
            # Get services with optional filtering
            services = SAMPLE_SERVICES.copy()
            
            # Apply category filter
            category = query_params.get('category', [None])[0]
            if category:
                services = [s for s in services if s['category'] == category]
            
            # Apply free tier filter
            free_tier_param = query_params.get('free_tier', [None])[0]
            if free_tier_param is not None:
                free_tier = free_tier_param.lower() == 'true'
                services = [s for s in services if s['free_tier_available'] == free_tier]
            
            # Apply search filter
            search = query_params.get('search', [None])[0]
            if search:
                search_lower = search.lower()
                services = [
                    s for s in services 
                    if search_lower in s['name'].lower() or search_lower in s['description'].lower()
                ]
            
            response_data = {
                'services': services,
                'total_count': len(services),
                'categories': CATEGORIES
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
