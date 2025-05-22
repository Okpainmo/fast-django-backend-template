from django.shortcuts import render

# Create your views here.
from ninja import Router, Schema
from typing import Optional
from datetime import datetime
from .models import User
from utils.coded_error_handlers import error_handler_404, error_handler_500
from utils.logger import logger
from django.http import JsonResponse
from utils.cookie_deploy_handler import deploy_auth_cookie

# from middlewares.global__auth_access_and_session_middleware import AuthBearer

log = logger()
user_router = Router()


class _pResponse(Schema):
    id: int
    name: Optional[str]
    email: str
    is_admin: bool
    is_active: bool
    created_at: datetime
    updated_at: datetime
    access_token: Optional[str] = None
    refresh_token: Optional[str] = None


class ResponseSpecs(Schema):
    response_message: str
    response: dict
    error: Optional[str] = None
    sessionStatus: Optional[str] = None

    class Config:
        exclude_none = True


@user_router.get("/", response=ResponseSpecs)
def user_base(request):
    return JsonResponse(
        {"response_message": "User domain is live!!!", "response": {"message": "OK!!!"}}
    )


@user_router.get("/{user_id}", response=ResponseSpecs)
def get_user_profile(request, user_id: int):
    """
    Get the profile of any user
    """
    try:
        user = User.objects.filter(id=user_id).first()

        if not user:
            log.error("User not found", user_id=user_id)
            return error_handler_404(f"user with id: '{user_id}' not found or does not exist")

        user_profile = {
            "id": user.id,
            "name": user.name or "",
            "email": user.email,
            "is_admin": user.is_admin,
            "is_active": user.is_active,
            "created_at": user.created_at,
            "updated_at": user.updated_at,
        }

        response_data = JsonResponse(
            {
                "response_message": "User profile retrieved successfully",
                "response": {
                    "user_profile": user_profile,
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
        log.error("Error retrieving user profile", error=str(e), user_id=user_id)
        return error_handler_500(e)
