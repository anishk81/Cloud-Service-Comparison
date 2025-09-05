# AWS Service Comparison App

A full-stack web application for comparing AWS services with detailed information about categories, features, and pricing.

## Architecture

- **Frontend**: React with TypeScript
- **Backend**: Python with FastAPI
- **Data**: AWS service information with categories, features, and pricing notes

## Project Structure

```
cloud-service-comparison/
├── frontend/          # React TypeScript application
├── backend/           # Python FastAPI server
├── docs/              # Documentation
└── README.md
```

## Getting Started

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the API server:
   ```bash
   uvicorn main:app --reload
   ```

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm start
   ```

## Features

- Browse AWS services by category
- Compare multiple services side-by-side
- Search and filter functionality
- Detailed service information including pricing notes
- Responsive design for mobile and desktop

## API Endpoints

- `GET /api/services` - Get all AWS services
- `GET /api/services/{service_id}` - Get specific service details
- `GET /api/categories` - Get all service categories
- `GET /api/services/category/{category}` - Get services by category
