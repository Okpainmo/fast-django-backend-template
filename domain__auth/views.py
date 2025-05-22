from django.shortcuts import render

# Create your views here.
from ninja import Router, Schema
from typing import Optional
from datetime import datetime
from django.contrib.auth.hashers import check_password, make_password
from domain__user.models import User
from utils.coded_error_handlers import error_handler_400, error_handler_403, error_handler_404, error_handler_500
from utils.generate_tokens import generate_tokens
from utils.cookie_deploy_handler import deploy_auth_cookie
from django.http import JsonResponse
from utils.logger import logger

log = logger()
auth_router = Router()

class InSpecs__LogIn(Schema):
    email: str
    password: str

class InSpecs__Register(Schema):
    name: str
    email: str
    password: str

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

@auth_router.get("/", response=ResponseSpecs)
def auth_base(request):
    return JsonResponse({
        "response_message": "Auth domain is live!!!",
        "response": {
            "message": "OK!!!"
        }
    })

@auth_router.post("/register", response=ResponseSpecs)
def register(request, payload: InSpecs__Register):
    """
    Register a new user
    """
    try:
        # Check if user already exists
        existing_user = User.objects.filter(email=payload.email).first()

        if existing_user:
            log.error("User already exists", email=payload.email)
            return error_handler_400(f"User with email: '{payload.email}' already exists")

        # Hash password
        hashed_password = make_password(payload.password)

        # Create new user
        new_user = User.objects.create(
            name=payload.name,
            email=payload.email,
            password=hashed_password,
            is_admin=False,  # Always set to False for security
            is_active=True
        )

        # Generate auth tokens
        tokens = generate_tokens({
            "user_id": new_user.id,
            "email": new_user.email,
            "token_type": "auth"
        })

        # log.info("auth tokens inside auth(register) controller", data=tokens)
        log.info("auth_cookie", data=tokens.get("auth_cookie"))

        if tokens:
            # Update user with tokens
            new_user.access_token = tokens.get('access_token')
            new_user.refresh_token = tokens.get('refresh_token')
            new_user.save()

            response_data = JsonResponse({
                "response_message": "User registered successfully",
                "response": {
                    "user_profile": {
                        "id": new_user.id,
                        "name": new_user.name,
                        "email": new_user.email,
                        "is_admin": new_user.is_admin,
                        "is_active": new_user.is_active,
                        "created_at": new_user.created_at,
                        "updated_at": new_user.updated_at,
                    },
                    "access_token": tokens.get('access_token'),
                    "refresh_token": tokens.get('refresh_token')
                }
            })

            # Deploy auth cookie
            deploy_auth_cookie({
                "response": response_data,
                "auth_cookie": tokens.get('auth_cookie')
            })
            
            return response_data

    except Exception as e:
        log.error("Error during registration", error=str(e), email=payload.email)
        return error_handler_500(e)

@auth_router.post("/log-in", response=ResponseSpecs)
def login(request, payload: InSpecs__LogIn):
    """
    Log in a new user
    """
    try:
        existing_user = User.objects.filter(email=payload.email).first()

        if not existing_user:
            log.error("User not found", email=payload.email)
            return error_handler_404(f"user with email: '{payload.email}' not found or does not exist")

        if not check_password(payload.password, existing_user.password):
            log.error("Incorrect password", email=payload.email)
            return error_handler_403("incorrect password: login unsuccessful")

        # Generate auth tokens
        tokens = generate_tokens({
            "user_id": existing_user.id,
            "email": existing_user.email,
            "token_type": "auth"
        })

        if tokens:
            # Update user with new tokens
            existing_user.access_token = tokens.get('access_token')
            existing_user.refresh_token = tokens.get('refresh_token')
            existing_user.save()           

            response_data = JsonResponse({
                "response_message": "User logged in successfully",
                "response": {
                    "user_profile": {
                        "id": existing_user.id,
                        "name": existing_user.name or "",
                        "email": existing_user.email,
                        "is_admin": existing_user.is_admin,
                        "is_active": existing_user.is_active,
                        "created_at": existing_user.created_at,
                        "updated_at": existing_user.updated_at,
                    },
                    "access_token": tokens.get('access_token'),
                    "refresh_token": tokens.get('refresh_token')
                }
            })

             # Deploy auth cookie
            deploy_auth_cookie({
                "response": response_data,
                "auth_cookie": tokens.get('auth_cookie')
            })

            return response_data

    except Exception as e:
        log.error("Error during login", error=str(e), email=payload.email)
        return error_handler_500(e)
