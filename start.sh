#!/bin/bash
# Intersect FHIR API - Quick Start Script

echo "🏥 Intersect FHIR API - Quick Start"
echo "=================================="
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "✅ Created .env file"
    echo "⚠️  Please edit .env with your configuration"
    echo ""
fi

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed"
    echo "Please install Docker: https://docs.docker.com/get-docker/"
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed"
    echo "Please install Docker Compose: https://docs.docker.com/compose/install/"
    exit 1
fi

echo "🐳 Starting Docker containers..."
docker-compose up -d

echo ""
echo "⏳ Waiting for services to start..."
sleep 5

echo ""
echo "✅ Intersect FHIR API is running!"
echo ""
echo "📍 Access points:"
echo "   - API: http://localhost:8000"
echo "   - API Docs: http://localhost:8000/docs"
echo "   - Health Check: http://localhost:8000/health"
echo "   - MongoDB UI: http://localhost:8081 (admin/admin123)"
echo ""
echo "📚 Next steps:"
echo "   1. Visit http://localhost:8000/docs"
echo "   2. Register a user at /api/v1/auth/register"
echo "   3. Get a token at /api/v1/auth/login"
echo "   4. Start creating FHIR resources!"
echo ""
echo "🛑 To stop: docker-compose down"
echo "📋 To view logs: docker-compose logs -f api"
echo ""
