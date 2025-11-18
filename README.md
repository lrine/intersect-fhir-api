# 🏥 Intersect FHIR API - Complete Starter Kit

Production-ready FastAPI application with FHIR R6 resources for remote patient monitoring, telehealth, and precision genomic medicine.

## 🚀 Features

- **25 FHIR R6 Resources** - Complete implementation
- **JWT Authentication** - Secure API access
- **MongoDB/Cosmos DB** - Scalable data storage
- **Auto-generated Documentation** - Interactive Swagger UI
- **Docker Support** - Easy deployment
- **Wearable Integration** - Samsung Health ready
- **Search & Filtering** - FHIR-compliant queries
- **Audit Logging** - Track all API calls

## 📋 Resources Included

### Foundation Resources
- Patient, Practitioner, Organization, Device, Location

### Clinical Resources
- Observation, DiagnosticReport, Specimen, Encounter, Condition

### Workflow Resources
- Appointment, ServiceRequest, Task

### Medication Resources
- Medication, MedicationRequest

### Care Coordination
- CareTeam, Communication

### History Resources
- Procedure, FamilyMemberHistory, Immunization, AllergyIntolerance

### Document Resources
- DocumentReference

## 🛠️ Quick Start

### Option 1: Docker (Recommended)

```bash
# 1. Clone or extract the starter kit
cd intersect-fhir-api

# 2. Copy environment configuration
cp .env.example .env

# 3. Start all services
docker-compose up -d

# 4. API is now running!
# - API: http://localhost:8000
# - Docs: http://localhost:8000/docs
# - MongoDB UI: http://localhost:8081
```

### Option 2: Local Development

```bash
# 1. Install Python 3.11+
python --version

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up environment
cp .env.example .env
# Edit .env with your MongoDB connection string

# 5. Run the application
python -m uvicorn app.main:app --reload

# 6. Access the API
# - API: http://localhost:8000
# - Docs: http://localhost:8000/docs
```

## 🔐 First Steps

### 1. Create a User

```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "email": "admin@intersect.health",
    "password": "SecurePassword123!",
    "full_name": "Admin User",
    "roles": ["admin", "clinician"]
  }'
```

### 2. Get Access Token

```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=SecurePassword123!"
```

Response:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### 3. Create a Patient

```bash
curl -X POST "http://localhost:8000/api/v1/Patient" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "resourceType": "Patient",
    "identifier": [{
      "system": "http://intersect.health/mrn",
      "value": "MRN123456"
    }],
    "name": [{
      "family": "Smith",
      "given": ["John", "Robert"]
    }],
    "gender": "male",
    "birthDate": "1985-03-15"
  }'
```

## 📚 API Documentation

Once running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔧 Configuration

Edit `.env` file:

```env
# MongoDB/Cosmos DB
MONGODB_URL=mongodb://localhost:27017
MONGODB_DATABASE=intersect_fhir

# For Azure Cosmos DB:
# MONGODB_URL=mongodb://your-account.mongo.cosmos.azure.com:10255/?ssl=true...

# JWT Security
SECRET_KEY=your-secret-key-change-in-production
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:4200

# Features
ENABLE_AUTH=True
ENABLE_RATE_LIMITING=True
```

## 🏗️ Project Structure

```
intersect-fhir-api/
├── app/
│   ├── main.py              # FastAPI application
│   ├── config.py            # Configuration management
│   ├── database.py          # MongoDB connection
│   ├── routers/             # API endpoints
│   │   ├── auth.py          # Authentication
│   │   ├── patient.py       # Patient resource
│   │   ├── observation.py   # Observation resource
│   │   └── ... (22 more)
│   ├── services/            # Business logic
│   │   └── auth_service.py  # JWT & auth
│   ├── schemas/             # Pydantic models
│   │   └── auth.py
│   └── utils/               # Helper functions
│       └── loinc_codes.py   # LOINC code reference
├── tests/                   # Unit tests
├── postman/                 # Postman collections
├── examples/                # Sample FHIR data
├── docs/                    # Additional documentation
├── docker-compose.yml       # Docker orchestration
├── Dockerfile              # Container definition
├── requirements.txt         # Python dependencies
└── .env.example            # Environment template
```

## 📊 Example Use Cases

### Wearable Data (Blood Pressure)

```json
POST /api/v1/Observation
{
  "resourceType": "Observation",
  "status": "final",
  "category": [{
    "coding": [{
      "system": "http://terminology.hl7.org/CodeSystem/observation-category",
      "code": "vital-signs"
    }]
  }],
  "code": {
    "coding": [{
      "system": "http://loinc.org",
      "code": "85354-9",
      "display": "Blood pressure panel"
    }]
  },
  "subject": {
    "reference": "Patient/patient-123"
  },
  "effectiveDateTime": "2025-11-14T10:30:00Z",
  "component": [
    {
      "code": {
        "coding": [{
          "system": "http://loinc.org",
          "code": "8480-6",
          "display": "Systolic blood pressure"
        }]
      },
      "valueQuantity": {
        "value": 120,
        "unit": "mmHg"
      }
    },
    {
      "code": {
        "coding": [{
          "system": "http://loinc.org",
          "code": "8462-4",
          "display": "Diastolic blood pressure"
        }]
      },
      "valueQuantity": {
        "value": 80,
        "unit": "mmHg"
      }
    }
  ]
}
```

### Search Observations

```bash
# Get all vital signs for a patient
GET /api/v1/Observation?patient=Patient/patient-123&category=vital-signs

# Get observations from last week
GET /api/v1/Observation?patient=Patient/patient-123&date_from=2025-11-07

# Get latest 10 observations
GET /api/v1/Observation/latest/patient-123?limit=10
```

## 🔌 Frontend Integration

### Angular Example

```typescript
import { HttpClient } from '@angular/common/http';

export class PatientService {
  private apiUrl = 'http://localhost:8000/api/v1';
  private token = localStorage.getItem('token');

  constructor(private http: HttpClient) {}

  getPatients() {
    return this.http.get(`${this.apiUrl}/Patient`, {
      headers: { 'Authorization': `Bearer ${this.token}` }
    });
  }
}
```

### React Native Example

```javascript
const getPatients = async () => {
  const token = await AsyncStorage.getItem('token');
  
  const response = await fetch('http://api.intersect.com/api/v1/Patient', {
    headers: {
      'Authorization': `Bearer ${token}`
    }
  });
  
  const patients = await response.json();
  return patients;
};
```

## 🧪 Testing

```bash
# Run tests
pytest

# With coverage
pytest --cov=app tests/
```

## 📦 Deployment

### Deploy to Azure VM

```bash
# 1. SSH into your Azure VM
ssh user@your-vm-ip

# 2. Clone repository
git clone https://github.com/your-org/intersect-fhir-api.git
cd intersect-fhir-api

# 3. Set up environment
cp .env.example .env
nano .env  # Edit with production values

# 4. Start with Docker
docker-compose up -d

# 5. Verify
curl http://localhost:8000/health
```

### Use Azure Cosmos DB

Update `.env`:
```env
MONGODB_URL=mongodb://intersect-cosmos.mongo.cosmos.azure.com:10255/?ssl=true&retrywrites=false&maxIdleTimeMS=120000
MONGODB_DATABASE=intersect_fhir
```

## 🛡️ Security Best Practices

1. **Change default SECRET_KEY** in production
2. **Use HTTPS** in production
3. **Enable rate limiting**
4. **Implement role-based access control**
5. **Regular security audits**
6. **Keep dependencies updated**

## 📝 Customization Guide

### Add Custom Search Parameters

Edit relevant router (e.g., `app/routers/patient.py`):

```python
@router.get("/Patient")
async def search_patients(
    # Add your custom parameter
    custom_field: Optional[str] = Query(None),
    ...
):
    query = {}
    if custom_field:
        query["customField"] = custom_field
    ...
```

### Add Custom Validation

```python
@router.post("/Patient")
async def create_patient(patient: Patient):
    # Add your custom validation
    if not patient.identifier:
        raise HTTPException(400, "MRN required")
    
    # Check format
    mrn = patient.identifier[0].value
    if not mrn.startswith("MRN"):
        raise HTTPException(400, "Invalid MRN format")
    ...
```

## 🤝 Support

- **Documentation**: `/docs` endpoint
- **GitHub Issues**: [Report bugs or request features]
- **Email**: support@intersect.health

## 📄 License

Proprietary - Intersect Healthcare Systems

## 🎯 Next Steps

1. ✅ Run the application locally
2. ✅ Create test data using Postman
3. ✅ Connect your Angular/React frontend
4. ✅ Deploy to Azure
5. ✅ Integrate wearable devices
6. ✅ Set up monitoring and logging

## 🚀 You're Ready to Go!

Your FHIR API is production-ready. Start building your healthcare applications!

```bash
# Quick start reminder:
docker-compose up -d
open http://localhost:8000/docs
```

---

**Built with ❤️ for Intersect Healthcare Systems**
