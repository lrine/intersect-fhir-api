"""
Enumerations for the application
"""
from enum import Enum


class UserRole(str, Enum):
    """
    User roles for role-based access control

    Note: Patients access a separate patient portal and are not part of this admin system
    """
    ADMIN = "admin"
    PRACTITIONER = "practitioner"
    NURSE = "nurse"
    SCHEDULER = "scheduler"
    FINANCE = "finance"
