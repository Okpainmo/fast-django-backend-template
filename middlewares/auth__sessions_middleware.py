"""
Session Management Middleware for Django

This middleware handles session validation and management for authenticated routes.
It works in conjunction with the access middleware to provide a complete authentication system.

The middleware performs the following checks:
1. Validates auth cookies and their format
2. Verifies user credentials against stored hashes
3. Validates refresh tokens for session state
4. Manages session expiration and termination
5. Provides session status tracking

Excluded paths:
- /api/v1/auth/log-in
- /api/v1/auth/register
- /, /api, /api/
"""

import jwt
from django.conf import settings
from django.contrib.auth.hashers import check_password
from utils.coded_error_handlers import error_handler_400, error_handler_401, error_handler_404
from utils.logger import logger
from domain__user.models import User
from django.utils.deprecation import MiddlewareMixin


log = logger()


class Auth_SessionsMiddleware(MiddlewareMixin):
    def process_request(self, request):
        excluded_paths__starts_with = [
            "/api/v1/auth/log-in",
            "/api/v1/auth/register",
        ]

        excluded_paths__exact_checks = [
            "/",
            "/api",
            "/api/",
        ]

        log.info("request path", path=request.path)

        if any(request.path == path for path in excluded_paths__exact_checks) or any(request.path.startswith(path) for path in excluded_paths__starts_with):
            return None  # allow through

        # ==================================================================================
        # check for auth_cookie, and reject if the cookie is not available on the request
        # ==================================================================================
        auth_cookie = request.COOKIES.get("Fast_Django_Backend_Template")

        if not auth_cookie:
            log.error("auth_cookie not available")
            return error_handler_401("Request rejected - user does not have access to this route")

        # ==================================================================================
        # check for the required request headers and perform further query
        # ==================================================================================
        email = request.headers.get("email")
        authorization = request.headers.get("authorization")

        if not email or not authorization:
            log.error(
                "Request header data missing", email=email, has_authorization=bool(authorization)
            )
            return error_handler_400("Email, and authorization header data must be provided on the request")

        # ==================================================================================
        # OPTIONAL: further query on auth_cookie, to ensure it contains the correct user credential that was
        # written into it before it was previously sent to the user.
        # ==================================================================================
        try:
            auth_cookie_secret = auth_cookie.split("_____")[2]
            hashed_email = auth_cookie.split("_____")[1]
        except IndexError:
            log.error("Invalid auth cookie format", auth_cookie=auth_cookie[:10] + "...")
            return error_handler_401("Request rejected - invalid auth cookie format")

        if settings.SECRET_KEY != auth_cookie_secret or not check_password(email, hashed_email):
            log.error(
                "Invalid auth cookie",
                email=email,
                has_valid_secret=settings.SECRET_KEY == auth_cookie_secret,
                has_valid_email=check_password(email, hashed_email),
            )
            return error_handler_401("Request rejected - invalid auth_cookie detected")

        # =================================================================================
        # Get the user's refresh token from the DB, and verify that it's still valid
        # and not expired. If expired, reject request and end the user session. This is helpful,
        # in case the above cookie-check is disabled or in-active - e.g. for mobile environments.
        #
        # P.S: Both the cookie and refresh_token are set to expire within 24 hours.
        # =================================================================================

        # now proceed to check for the user
        user = User.objects.filter(email=email).first()

        if not user:
            log.error("User not found", email=email)
            return error_handler_404(f"User with email: '{email}' not found or does not exist.")

        try:
            jwt.decode(user.refresh_token, settings.SECRET_KEY, algorithms=["HS256"])
            # jwt_payload = jwt.decode(user.refresh_token, settings.SECRET_KEY, algorithms=["HS256"])
            # log.info("refresh_token jwt_payload", jwt_payload__refresh=jwt_payload)
        except jwt.ExpiredSignatureError:
            log.error("Token expired", refresh_token=user.refresh_token[:10] + "...")

            # ==================================================================================
            # if you track user sessions, handle ENDING/TERMINATING the user session in DB here
            # ==================================================================================

            session_status = f"EXPIRED SESSION: session terminated for '{email}'"
            log.info(session_status)

            return error_handler_401("Access denied - session is expired, please re-authenticate")
        except jwt.InvalidTokenError:
            log.error("Token expired", refresh_token=user.refresh_token[:10] + "...")
            return error_handler_401("Access denied - invalid token")

        session_status = "USER SESSION IS ACTIVE"
        log.info("session_status", session_status=session_status)

        # ==================================================================================
        # if you track user sessions, handle RENEWING the user session in DB here
        # ==================================================================================

        return None  # continue processing

