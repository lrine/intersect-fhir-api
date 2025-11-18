"""
Routers Package
Exports all FHIR resource routers
"""
from app.routers import auth
from app.routers import patient
from app.routers import practitioner
from app.routers import organization
from app.routers import device
from app.routers import location
from app.routers import observation
from app.routers import diagnostic_report
from app.routers import specimen
from app.routers import encounter
from app.routers import appointment
from app.routers import service_request
from app.routers import medication_request
from app.routers import medication
from app.routers import care_team
from app.routers import condition
from app.routers import procedure
from app.routers import family_member_history
from app.routers import immunization
from app.routers import allergy_intolerance
from app.routers import document_reference
from app.routers import communication
from app.routers import task

__all__ = [
    "auth",
    "patient",
    "practitioner",
    "organization",
    "device",
    "location",
    "observation",
    "diagnostic_report",
    "specimen",
    "encounter",
    "appointment",
    "service_request",
    "medication_request",
    "medication",
    "care_team",
    "condition",
    "procedure",
    "family_member_history",
    "immunization",
    "allergy_intolerance",
    "document_reference",
    "communication",
    "task",
]
