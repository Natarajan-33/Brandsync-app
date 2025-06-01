# BrandSync Backend

This is the backend API for the BrandSync application, built with FastAPI.

## Features

- Influencer management and discovery
- Natural language search using sentence transformers and ChromaDB
- RESTful API endpoints

## Setup

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. Clone the repository (if you haven't already)

2. Navigate to the backend directory:
   ```
   cd backend
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Running the Application

1. Start the FastAPI server:
   ```
   python server.py
   ```

2. The API will be available at `http://localhost:8000`

3. Access the API documentation at `http://localhost:8000/docs`

## API Endpoints

### Influencers

- `GET /influencers/`: Get all influencers
- `GET /influencers/search?q=...`: Search influencers using natural language

## Testing

Run the tests using pytest:

```
pip install pytest
pytest
```

## Frontend Integration

The frontend is configured to connect to the backend at `http://localhost:8000`. Make sure the backend server is running when using the frontend application.

## Future Scope

- Add authentication and authorization
- Implement database persistence
- Add more advanced filtering and sorting options
- Implement campaign management features
