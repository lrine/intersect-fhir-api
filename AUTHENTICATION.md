# Authentication System

## Overview

The Intersect FHIR API uses role-based JWT authentication for secure access to admin system resources.

**Note:** Patients access a separate patient portal and are not part of this admin authentication system.

## User Roles

The system supports the following roles:

- `admin` - Full system access
- `practitioner` - Healthcare providers
- `nurse` - Nursing staff
- `scheduler` - Appointment and scheduling staff
- `finance` - Financial and billing staff

## User Model

Users are stored in MongoDB with the following structure:

```json
{
  "_id": "user@example.com",
  "email": "user@example.com",
  "password_hash": "bcrypt_hash",
  "first_name": "John",
  "last_name": "Doe",
  "role": "practitioner",
  "created_at": "2024-01-01T00:00:00",
  "is_active": true
}
```

## API Endpoints

### 1. Register User

**POST** `/api/v1/auth/register`

Create a new user account.

**Request Body:**
```json
{
  "email": "doctor@hospital.com",
  "password": "securePassword123",
  "first_name": "Jane",
  "last_name": "Smith",
  "role": "practitioner"
}
```

**Response:**
```json
{
  "_id": "doctor@hospital.com",
  "email": "doctor@hospital.com",
  "first_name": "Jane",
  "last_name": "Smith",
  "role": "practitioner",
  "created_at": "2024-01-01T00:00:00",
  "is_active": true
}
```

### 2. Login

**POST** `/api/v1/auth/login`

Authenticate and receive JWT token.

**Request Body:**
```json
{
  "email": "doctor@hospital.com",
  "password": "securePassword123"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "_id": "doctor@hospital.com",
    "email": "doctor@hospital.com",
    "first_name": "Jane",
    "last_name": "Smith",
    "role": "practitioner",
    "created_at": "2024-01-01T00:00:00",
    "is_active": true
  }
}
```

### 3. Get Current User Profile

**GET** `/api/v1/auth/me`

Get authenticated user's profile information.

**Headers:**
```
Authorization: Bearer <your-token>
```

**Response:**
```json
{
  "_id": "doctor@hospital.com",
  "email": "doctor@hospital.com",
  "first_name": "Jane",
  "last_name": "Smith",
  "role": "practitioner",
  "created_at": "2024-01-01T00:00:00",
  "is_active": true
}
```

## Using Authentication in Routes

### Protected Routes

All FHIR resource endpoints are protected and require authentication:

```python
from fastapi import Depends
from app.routers.auth import get_current_user

@router.get("/Patient")
async def get_patients(current_user: dict = Depends(get_current_user)):
    # User is authenticated
    # current_user contains user data including role
    pass
```

### Role-Based Access Control

Use permission decorators to restrict access by role:

```python
from fastapi import Depends
from app.models.enums import UserRole
from app.middleware.permissions import require_role, require_any_role

# Require specific role
@router.delete("/users/{user_id}")
async def delete_user(
    user_id: str,
    user: dict = Depends(require_role(UserRole.ADMIN))
):
    # Only admins can access this endpoint
    pass

# Require any of multiple roles
@router.get("/medical-records")
async def get_medical_records(
    user: dict = Depends(require_any_role([UserRole.PRACTITIONER, UserRole.NURSE]))
):
    # Practitioners or nurses can access this endpoint
    pass

# Convenience admin-only decorator
from app.middleware.permissions import require_admin

@router.post("/system-settings")
async def update_settings(
    settings: dict,
    admin: dict = Depends(require_admin)
):
    # Only admins can access
    pass
```

## JWT Token Details

### Token Payload

The JWT token contains:

```json
{
  "user_id": "user@example.com",
  "email": "user@example.com",
  "role": "practitioner",
  "exp": 1234567890
}
```

### Token Configuration

Token expiration and secret key are configured in `app/config.py`:

```python
secret_key: str = "your-secret-key"  # Change in production!
algorithm: str = "HS256"
access_token_expire_minutes: int = 30
```

## Security Features

1. **Password Hashing**: Uses bcrypt for secure password storage
2. **JWT Tokens**: Stateless authentication with signed tokens
3. **Role-Based Access**: Fine-grained permissions system
4. **Token Expiration**: Configurable token lifetime
5. **Active User Check**: Inactive accounts cannot authenticate

## Development Setup

1. Ensure MongoDB is running
2. Set environment variables in `.env`:
   ```
   SECRET_KEY=your-secret-key-change-in-production
   MONGODB_URL=mongodb://localhost:27017
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:
   ```bash
   python -m app.main
   ```

## Testing Authentication

### Using curl

```bash
# Register a user
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password123",
    "first_name": "Test",
    "last_name": "User",
    "role": "practitioner"
  }'

# Login
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password123"
  }'

# Get profile (use token from login response)
curl -X GET http://localhost:8000/api/v1/auth/me \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

### Using the Swagger UI

1. Navigate to http://localhost:8000/docs
2. Click "Authorize" button
3. Enter your Bearer token
4. Test protected endpoints

## Production Considerations

1. **Change SECRET_KEY**: Use a strong, random secret key in production
2. **HTTPS Only**: Always use HTTPS in production
3. **Token Rotation**: Consider implementing refresh tokens for long sessions
4. **Rate Limiting**: Add rate limiting to prevent brute force attacks
5. **Password Policy**: Enforce strong password requirements
6. **Audit Logging**: Log authentication attempts and access
