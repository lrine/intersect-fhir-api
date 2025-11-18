# 🚀 Setup Guide - Intersect FHIR API

Complete step-by-step guide to get your FHIR API running.

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Quick Start (Docker)](#quick-start-docker)
3. [Local Development Setup](#local-development-setup)
4. [Azure Deployment](#azure-deployment)
5. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Required
- **Docker** (v20.10+) and **Docker Compose** (v2.0+)
  - Download: https://docs.docker.com/get-docker/
- **Git** (for cloning/updating)

### Optional (for local development)
- **Python 3.11+**
- **MongoDB 7.0+** (if not using Docker)

---

## Quick Start (Docker)

**This is the fastest way to get started!**

### Step 1: Extract Files

```bash
# Extract the starter kit
unzip intersect-fhir-api.zip
cd intersect-fhir-api
```

### Step 2: Configure Environment

```bash
# Copy environment template
cp .env.example .env

# Edit if needed (optional for local testing)
nano .env
```

### Step 3: Start Everything

```bash
# Use the quick start script
./start.sh

# Or manually:
docker-compose up -d
```

### Step 4: Verify It's Running

Open your browser:
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

You should see: `{"status": "healthy"}`

### Step 5: Create Your First User

Go to http://localhost:8000/docs and use the interactive API:

1. Find `/api/v1/auth/register`
2. Click "Try it out"
3. Use this JSON:

```json
{
  "username": "admin",
  "email": "admin@intersect.health",
  "password": "Admin123!",
  "full_name": "Admin User",
  "roles": ["admin", "clinician"]
}
```

4. Click "Execute"

### Step 6: Get Access Token

1. Find `/api/v1/auth/login`
2. Click "Try it out"
3. Enter:
   - username: `admin`
   - password: `Admin123!`
4. Copy the `access_token` from the response

### Step 7: Authorize

1. Click the "Authorize" button at the top
2. Enter: `Bearer YOUR_TOKEN_HERE`
3. Click "Authorize"

**You're now authenticated!** Try creating a Patient or Observation.

---

## Local Development Setup

**For developers who want to modify the code.**

### Step 1: Install Python

```bash
# Check Python version
python3 --version  # Should be 3.11+

# If not installed, download from python.org
```

### Step 2: Create Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate  # On Mac/Linux
# OR
venv\Scripts\activate  # On Windows
```

### Step 3: Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 4: Set Up MongoDB

**Option A: Use Docker (easiest)**
```bash
docker run -d -p 27017:27017 --name mongodb mongo:7.0
```

**Option B: Install MongoDB locally**
- Download: https://www.mongodb.com/try/download/community
- Follow installation instructions for your OS

### Step 5: Configure Environment

```bash
cp .env.example .env
nano .env
```

Update:
```env
MONGODB_URL=mongodb://localhost:27017
SECRET_KEY=your-secret-key-here
```

### Step 6: Run the Application

```bash
# Development mode (auto-reload)
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Or production mode
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Step 7: Access the API

Visit: http://localhost:8000/docs

---

## Azure Deployment

**Deploy to your Azure VM**

### Prerequisites
- Azure VM (Ubuntu 20.04+)
- SSH access to VM
- Domain name (optional but recommended)

### Step 1: Connect to Azure VM

```bash
ssh your-username@your-vm-ip
```

### Step 2: Install Docker

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Add user to docker group
sudo usermod -aG docker $USER

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Verify
docker --version
docker-compose --version
```

### Step 3: Upload Application

**Option A: Using Git**
```bash
git clone https://github.com/your-org/intersect-fhir-api.git
cd intersect-fhir-api
```

**Option B: Using SCP**
```bash
# On your local machine
scp -r intersect-fhir-api your-username@your-vm-ip:~/
```

### Step 4: Configure for Production

```bash
cd intersect-fhir-api
cp .env.example .env
nano .env
```

Update for production:
```env
DEBUG=False
ENVIRONMENT=production
SECRET_KEY=<generate-with-openssl-rand-hex-32>

# For Azure Cosmos DB
MONGODB_URL=mongodb://your-cosmos-account.mongo.cosmos.azure.com:10255/?ssl=true&retrywrites=false...
MONGODB_DATABASE=intersect_fhir

# Update CORS for your domain
ALLOWED_ORIGINS=https://your-frontend-domain.com
```

### Step 5: Start Services

```bash
docker-compose up -d
```

### Step 6: Configure Nginx (Optional but Recommended)

```bash
# Install Nginx
sudo apt install nginx -y

# Create config
sudo nano /etc/nginx/sites-available/intersect-fhir-api
```

Add:
```nginx
server {
    listen 80;
    server_name api.your-domain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Enable and restart:
```bash
sudo ln -s /etc/nginx/sites-available/intersect-fhir-api /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### Step 7: Set Up SSL (Recommended)

```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx -y

# Get certificate
sudo certbot --nginx -d api.your-domain.com
```

### Step 8: Configure Firewall

```bash
# Allow HTTP and HTTPS
sudo ufw allow 80
sudo ufw allow 443
sudo ufw enable
```

### Step 9: Verify Deployment

```bash
# Check service status
docker-compose ps

# Check logs
docker-compose logs api

# Test API
curl https://api.your-domain.com/health
```

---

## Azure Cosmos DB Setup

### Step 1: Create Cosmos DB Account

1. Go to Azure Portal
2. Create new resource → Azure Cosmos DB
3. Choose "Azure Cosmos DB for MongoDB"
4. Configure:
   - Resource group: `intersect-resources`
   - Account name: `intersect-cosmos`
   - API: MongoDB
   - Location: Same as your VM

### Step 2: Get Connection String

1. Go to your Cosmos DB account
2. Settings → Connection String
3. Copy "PRIMARY CONNECTION STRING"

### Step 3: Update .env

```env
MONGODB_URL=mongodb://intersect-cosmos:XXXXX==@intersect-cosmos.mongo.cosmos.azure.com:10255/?ssl=true&retrywrites=false&maxIdleTimeMS=120000&appName=@intersect-cosmos@
```

### Step 4: Restart Application

```bash
docker-compose down
docker-compose up -d
```

---

## Troubleshooting

### Port Already in Use

**Problem**: `Error: port 8000 already in use`

**Solution**:
```bash
# Find process using port
lsof -i :8000

# Kill the process
kill -9 <PID>

# Or change port in .env
PORT=8001
```

### MongoDB Connection Failed

**Problem**: `Could not connect to MongoDB`

**Solution**:
```bash
# Check if MongoDB is running
docker ps | grep mongo

# Check logs
docker logs intersect-mongodb

# Restart MongoDB
docker-compose restart mongodb
```

### Import Errors

**Problem**: `ModuleNotFoundError: No module named 'fhir'`

**Solution**:
```bash
# Reinstall dependencies
pip install -r requirements.txt

# Or if using Docker
docker-compose build --no-cache
docker-compose up -d
```

### Authentication Not Working

**Problem**: `Could not validate credentials`

**Solution**:
```bash
# Generate new SECRET_KEY
openssl rand -hex 32

# Update .env with new key
# Restart application
docker-compose restart api
```

### CORS Errors

**Problem**: Frontend can't access API

**Solution**:
Update `.env`:
```env
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:4200,https://your-domain.com
```

Restart:
```bash
docker-compose restart api
```

---

## Next Steps

1. ✅ Read the main [README.md](README.md)
2. ✅ Explore the API documentation at `/docs`
3. ✅ Create test data using the examples in `/examples`
4. ✅ Connect your frontend applications
5. ✅ Set up monitoring and logging

---

## Support

- **Documentation**: Check `/docs` endpoint
- **Examples**: See `/examples` directory
- **Common Issues**: This troubleshooting guide
- **Email**: support@intersect.health

---

**You're all set! Start building amazing healthcare applications! 🚀**
