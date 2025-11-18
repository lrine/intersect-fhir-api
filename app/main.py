"""
Intersect FHIR API - Main Application
FastAPI application with FHIR R6 resource endpoints
"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import logging
import time

from app.config import settings
from app.database import connect_to_database, close_database_connection

# Import routers (we'll create these next)
from app.routers import (
    auth,
    patient,
    practitioner,
    organization,
    device,
    location,
    observation,
    diagnostic_report,
    specimen,
    encounter,
    appointment,
    service_request,
    medication_request,
    medication,
    care_team,
    condition,
    procedure,
    family_member_history,
    immunization,
    allergy_intolerance,
    document_reference,
    communication,
    task,
)

# Configure logging
logging.basicConfig(
    level=settings.log_level,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan handler
    Manages startup and shutdown events
    """
    # Startup
    logger.info("🚀 Starting Intersect FHIR API...")
    await connect_to_database()
    logger.info(f"✅ Application started successfully on {settings.host}:{settings.port}")
    
    yield
    
    # Shutdown
    logger.info("Shutting down Intersect FHIR API...")
    await close_database_connection()
    logger.info("✅ Application shut down successfully")


# Create FastAPI application
app = FastAPI(
    title=settings.app_name,
    description="""
    ## Intersect Healthcare Systems - FHIR R6 API
    
    A comprehensive FHIR R6 compliant API for:
    - Remote Patient Monitoring
    - Telehealth Services
    - Precision Genomic Medicine
    - Maternal Health Monitoring
    
    ### Features:
    - 25 FHIR R6 Resources
    - Wearable Device Integration
    - Genomics Report Processing
    - Real-time Vital Signs Monitoring
    - JWT Authentication
    - Full CRUD Operations
    - FHIR Search Parameters
    
    ### Resources Available:
    - Foundation: Patient, Practitioner, Organization, Device, Location
    - Clinical: Observation, DiagnosticReport, Specimen, Encounter, Condition
    - Medications: Medication, MedicationRequest
    - Workflow: Appointment, ServiceRequest, Task
    - Care Coordination: CareTeam, Communication
    - History: Procedure, FamilyMemberHistory, Immunization, AllergyIntolerance
    - Documents: DocumentReference
    
    ### Authentication:
    Use the `/api/v1/auth/login` endpoint to get a JWT token.
    Then include the token in the Authorization header:
    ```
    Authorization: Bearer <your-token>
    ```
    """,
    version=settings.app_version,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all requests with timing"""
    start_time = time.time()
    
    response = await call_next(request)
    
    process_time = time.time() - start_time
    logger.info(
        f"{request.method} {request.url.path} "
        f"- Status: {response.status_code} "
        f"- Time: {process_time:.3f}s"
    )
    
    return response


# Exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler"""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error",
            "type": "InternalServerError"
        }
    )


# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    """API Root - Health check and info"""
    return {
        "message": "Intersect FHIR API",
        "version": settings.app_version,
        "status": "running",
        "fhir_version": "R6",
        "documentation": "/docs",
        "environment": settings.environment
    }


# Health check endpoint
@app.get("/health", tags=["Root"])
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "version": settings.app_version,
        "database": "connected"
    }


# Include routers
app.include_router(auth.router, prefix=settings.api_prefix, tags=["Authentication"])

# Foundation Resources
app.include_router(patient.router, prefix=settings.api_prefix, tags=["Patient"])
app.include_router(practitioner.router, prefix=settings.api_prefix, tags=["Practitioner"])
app.include_router(organization.router, prefix=settings.api_prefix, tags=["Organization"])
app.include_router(device.router, prefix=settings.api_prefix, tags=["Device"])
app.include_router(location.router, prefix=settings.api_prefix, tags=["Location"])

# Clinical Resources
app.include_router(observation.router, prefix=settings.api_prefix, tags=["Observation"])
app.include_router(diagnostic_report.router, prefix=settings.api_prefix, tags=["DiagnosticReport"])
app.include_router(specimen.router, prefix=settings.api_prefix, tags=["Specimen"])
app.include_router(encounter.router, prefix=settings.api_prefix, tags=["Encounter"])
app.include_router(condition.router, prefix=settings.api_prefix, tags=["Condition"])

# Workflow Resources
app.include_router(appointment.router, prefix=settings.api_prefix, tags=["Appointment"])
app.include_router(service_request.router, prefix=settings.api_prefix, tags=["ServiceRequest"])
app.include_router(task.router, prefix=settings.api_prefix, tags=["Task"])

# Medication Resources
app.include_router(medication.router, prefix=settings.api_prefix, tags=["Medication"])
app.include_router(medication_request.router, prefix=settings.api_prefix, tags=["MedicationRequest"])

# Care Coordination
app.include_router(care_team.router, prefix=settings.api_prefix, tags=["CareTeam"])
app.include_router(communication.router, prefix=settings.api_prefix, tags=["Communication"])

# History Resources
app.include_router(procedure.router, prefix=settings.api_prefix, tags=["Procedure"])
app.include_router(family_member_history.router, prefix=settings.api_prefix, tags=["FamilyMemberHistory"])
app.include_router(immunization.router, prefix=settings.api_prefix, tags=["Immunization"])
app.include_router(allergy_intolerance.router, prefix=settings.api_prefix, tags=["AllergyIntolerance"])

# Document Resources
app.include_router(document_reference.router, prefix=settings.api_prefix, tags=["DocumentReference"])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug
    )
