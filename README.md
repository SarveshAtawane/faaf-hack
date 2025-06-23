# Vendor Discovery Platform

A comprehensive AI-powered vendor discovery and automated enquiry system that helps businesses find local vendors, make automated calls for price inquiries, and manage delivery logistics through Porter integration.

## 🚀 Features

### Core Functionality
- **Intelligent Vendor Search**: Uses Google Maps API via SerpAPI to find local vendors based on product and location
- **Automated Voice Calls**: Integrates with Vapi.ai for automated vendor calls to collect pricing and availability
- **Real-time Updates**: WebSocket support for live enquiry status updates
- **Delivery Management**: Porter API integration for automated delivery order creation
- **Data Persistence**: MongoDB for storing vendor data, enquiries, and call records

### Key Components
- **FastAPI Backend**: High-performance async API with CORS support
- **AI Voice Assistant**: Vapi.ai integration for natural conversation with vendors
- **Maps Integration**: SerpAPI Google Maps for vendor discovery
- **Logistics API**: Porter integration for delivery management
- **Real-time Communication**: WebSocket endpoints for live updates

## 🏗️ Architecture

```
├── backend/vendor_app/
│   ├── main.py                 # FastAPI application entry point
│   ├── models/schemas.py       # Pydantic models for request/response
│   ├── routes/
│   │   ├── search.py          # Vendor search endpoints
│   │   ├── enquiry.py         # Enquiry management and calling
│   │   ├── vapi.py            # Vapi webhook handlers
│   │   ├── patch_vendor_data.py # Vendor data updates
│   │   └── place_porter_order.py # Porter delivery integration
│   ├── db/mongo.py            # MongoDB connection
│   ├── utils/
│   │   └── vapi_utils.py      # Vapi API utilities
│   └── requirements.txt       # Python dependencies
├── .env                       # Environment variables
└── docker-compose.yml         # Container orchestration
```

## 🛠️ Tech Stack

### Backend
- **FastAPI**: Modern Python web framework
- **MongoDB**: NoSQL database with PyMongo
- **Pydantic**: Data validation and serialization
- **Requests**: HTTP client for external APIs

### External APIs
- **Vapi.ai**: AI voice calling platform
- **SerpAPI**: Google Maps search integration
- **Porter**: Delivery and logistics API

### Infrastructure
- **Docker**: Containerization
- **Docker Compose**: Multi-container orchestration

## 📋 Prerequisites

- Python 3.8+
- Docker & Docker Compose
- MongoDB Atlas account
- Vapi.ai account and API keys
- SerpAPI account
- Porter API access

## 🚀 Quick Start

### 1. Clone Repository
```bash
git clone <repository-url>
cd vendor-discovery-platform
```

### 2. Environment Setup
Create `.env` file in the backend directory:
```bash
# Porter Configuration
PORTER_API_URL=https://pfe-apigw-uat.porter.in/v1/orders/create
PORTER_API_KEY=your_porter_api_key
REQUEST_TIMEOUT=30

# SerpAPI Configuration
SERP_API_API_KEY=your_serpapi_key
```

### 3. MongoDB Configuration
Update `backend/vendor_app/db/mongo.py` with your MongoDB connection string:
```python
client = MongoClient("your_mongodb_connection_string")
```

### 4. Vapi Configuration
Update API keys in `backend/vendor_app/utils/vapi_utils.py`:
```python
API_KEY = "your_vapi_api_key"
ASSISTANT_ID = "your_assistant_id"
PHONE_NUMBER_ID = "your_phone_number_id"
```

### 5. Start Services
```bash
docker-compose up -d
```

The application will be available at:
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs
- Frontend: http://localhost:3000

## 📡 API Endpoints

### Vendor Search
```http
POST /search
Content-Type: application/json

{
  "query": "fruit vendors",
  "location": "19.9975,73.7898"
}
```

### Create Enquiry
```http
POST /enquire
Content-Type: application/json

{
  "product": "apples",
  "location": "Mumbai",
  "vendors": [
    {
      "name": "Vendor Name",
      "phone": "+919876543210",
      "address": "Vendor Address",
      "lat": 19.9975,
      "lon": 73.7898
    }
  ],
  "additional_details": "Need 10kg organic apples"
}
```

### Get All Enquiries
```http
GET /enquiries
```

### Update Vendor Data
```http
PATCH /patch_vendor_data
Content-Type: application/json

{
  "collection_name": "apples_Mumbai",
  "vendor_id": "vendor_hash_id",
  "updates": {
    "price": "₹150/kg",
    "availability": "In Stock"
  }
}
```

### Porter Integration
```http
POST /api/create_porter_order
Content-Type: application/json

{
  "pickup_details": {
    "address": {
      "apartment_address": "123",
      "street_address1": "Main Street",
      "city": "Mumbai",
      "state": "Maharashtra",
      "pincode": "400001",
      "country": "India",
      "lat": 19.0760,
      "lng": 72.8777
    }
  },
  "delivery_instructions": {
    "instructions_list": [
      {
        "type": "text",
        "description": "Handle with care"
      }
    ]
  }
}
```

## 🔄 Workflow

1. **Vendor Discovery**: Search for vendors using product name and location
2. **Automated Calling**: System calls vendors using AI voice assistant
3. **Data Collection**: AI extracts pricing, availability, and other details
4. **Real-time Updates**: WebSocket broadcasts call results to connected clients
5. **Order Management**: Create delivery orders through Porter API

## 🔧 Configuration

### Vapi Assistant Configuration
The system uses specific assistant and phone number IDs for voice calls. Update these in `utils/vapi_utils.py`:

```python
ASSISTANT_ID = "98d8ba6f-d6e0-4e72-8100-d095a976c474"
PHONE_NUMBER_ID = "d4dfe093-298f-4033-90b6-27602eff8ef4"
```

### MongoDB Collections
The system creates dynamic collections based on product and location:
- Format: `{product}_{normalized_location}`
- Example: `apples_Mumbai` for apple vendors in Mumbai

### Webhook Configuration
Configure Vapi webhook endpoint in your Vapi dashboard:
```
POST /vapi/webhook
```

## 🔍 Monitoring & Debugging

### View API Documentation
Visit http://localhost:8000/docs for interactive API documentation

### Check Logs
```bash
docker-compose logs -f backend
```

### MongoDB Data
Monitor enquiries and call results in your MongoDB collections

## 🚨 Error Handling

The system includes comprehensive error handling for:
- API timeouts and failures
- Invalid phone numbers
- Missing vendor data
- Porter API errors
- Database connection issues

## 🔐 Security Considerations

- API keys stored in environment variables
- MongoDB connection secured with authentication
- CORS configured for cross-origin requests
- Input validation using Pydantic models

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Check the API documentation at `/docs`
- Review the logs for debugging information
