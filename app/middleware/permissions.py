"""
Role-based permission decorators for route protection

Usage examples:
    @router.get("/admin-only")
    async def admin_endpoint(user: dict = Depends(require_role(UserRole.ADMIN))):
        return {"message": "Admin only"}

    @router.get("/medical-staff")
    async def medical_endpoint(
        user: dict = Depends(require_any_role([UserRole.PRACTITIONER, UserRole.NURSE]))
    ):
        return {"message": "Medical staff only"}
"""
from fastapi import HTTPException, status, Depends
from typing import List, Callable
from app.models.enums import UserRole
from app.routers.auth import get_current_user


def require_role(required_role: UserRole) -> Callable:
    """
    Dependency factory to require a specific role

    Args:
        required_role: The role required to access the endpoint

    Returns:
        Dependency function that validates user has the required role

    Raises:
        HTTPException: If user doesn't have the required role

    Example:
        @router.get("/admin-dashboard")
        async def admin_dashboard(user: dict = Depends(require_role(UserRole.ADMIN))):
            return {"message": "Welcome Admin"}
    """
    async def role_checker(current_user: dict = Depends(get_current_user)) -> dict:
        user_role = current_user.get("role")

        if user_role != required_role.value:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied. Required role: {required_role.value}"
            )

        return current_user

    return role_checker


def require_any_role(allowed_roles: List[UserRole]) -> Callable:
    """
    Dependency factory to require any of the specified roles

    Args:
        allowed_roles: List of roles that are allowed to access the endpoint

    Returns:
        Dependency function that validates user has one of the allowed roles

    Raises:
        HTTPException: If user doesn't have any of the allowed roles

    Example:
        @router.get("/medical-records")
        async def medical_records(
            user: dict = Depends(require_any_role([UserRole.PRACTITIONER, UserRole.NURSE]))
        ):
            return {"message": "Medical staff access"}
    """
    async def role_checker(current_user: dict = Depends(get_current_user)) -> dict:
        user_role = current_user.get("role")

        if user_role not in [role.value for role in allowed_roles]:
            allowed_role_names = ", ".join([role.value for role in allowed_roles])
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied. Required roles: {allowed_role_names}"
            )

        return current_user

    return role_checker


def require_admin(current_user: dict = Depends(get_current_user)) -> dict:
    """
    Convenience dependency to require admin role

    Example:
        @router.delete("/users/{user_id}")
        async def delete_user(
            user_id: str,
            admin: dict = Depends(require_admin)
        ):
            return {"message": "User deleted"}
    """
    if current_user.get("role") != UserRole.ADMIN.value:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return current_user
