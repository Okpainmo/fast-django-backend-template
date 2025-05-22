from django.shortcuts import render
from ninja import Router, Schema
from typing import Optional
from datetime import datetime
from domain__user.models import User
from utils.coded_error_handlers import (
    error_handler_403,
    error_handler_404,
    error_handler_500,
    error_handler_400,
)
from utils.logger import logger

# from middlewares.auth__access_and_session_middleware import AuthBearer
from utils.generate_tokens import generate_tokens
from utils.cookie_deploy_handler import deploy_auth_cookie
from django.http import JsonResponse

log = logger()
admin_router = Router()

# class UserProfileResponse(Schema):
#     id: int
#     name: Optional[str]
#     email: str
#     is_admin: bool
#     is_active: bool
#     created_at: datetime
#     updated_at: datetime
#     access_token: str
#     refresh_token: str


class ResponseSpecs(Schema):
    response_message: str
    response: dict
    error: Optional[str] = None
    sessionStatus: Optional[str] = None

    class Config:
        exclude_none = True


@admin_router.get("/", response=ResponseSpecs)
def admin_base(request):
    return JsonResponse(
        {"response_message": "Admin domain is live!!!", "response": {"message": "OK!!!"}}
    )


@admin_router.patch("/deactivate-user/{user_id}", response=ResponseSpecs)
def deactivate_user(request, user_id: int):
    """
    Deactivate a user by ID (admin only)
    """
    try:
        # Get admin user from request (set by middleware)
        admin_user = request.user

        if not admin_user.is_admin:
            log.error(
                "Non-admin user attempted to deactivate user",
                action_attempted_by=f"user with id: {admin_user.id}",
            )
            return error_handler_403("You are not allowed to perform this action")

        # Find user to deactivate
        user_to_deactivate = User.objects.filter(id=user_id).first()

        if not user_to_deactivate:
            return error_handler_404(f"user with id: '{user_id}' not found or does not exist")

        if user_to_deactivate.is_active == False:
            return error_handler_400(f"user with id: '{user_id}' has already been de-activated")

        # Deactivate user
        user_to_deactivate.is_active = False
        user_to_deactivate.save()

        response_data = JsonResponse(
            {
                "response_message": "User deactivated successfully.",
                "response": {
                    "user_profile": {
                        "id": user_to_deactivate.id,
                        "name": user_to_deactivate.name or "",
                        "email": user_to_deactivate.email,
                        "is_admin": user_to_deactivate.is_admin,
                        "is_active": user_to_deactivate.is_active,
                        "created_at": user_to_deactivate.created_at,
                        "updated_at": user_to_deactivate.updated_at,
                    },
                    "access_token": getattr(request, "new_access_token", None),
                    "refresh_token": getattr(request, "new_refresh_token", None),
                },
            }
        )

        # Deploy auth cookie
        # deploy_auth_cookie({
        #     "response": response_data,
        #     "auth_cookie": getattr(request, "auth_cookie", None)
        # })

        return response_data

    except Exception as e:
        log.error("Error during user deactivation", error=str(e), user_id=user_id)
        return error_handler_500(e)
