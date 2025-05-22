"""
Global Django Middleware for authentication and session management

This middleware provides authentication and session management for all end-points
except for the log-in and register end-points respectively.

The middleware performs the following checks:
1. Validates the presence and format of auth cookies
2. Verifies request headers (email and authorization)
3. Validates refresh tokens and manages session state
4. Handles token renewal and user authentication
5. Provides user context to the view
"""

from ninja.security import HttpBearer
import jwt
from django.conf import settings
import json
from utils.generate_tokens import generate_tokens
from django.contrib.auth.hashers import check_password
from utils.coded_error_handlers import error_handler_400, error_handler_401, error_handler_404
from utils.logger import logger
from domain__user.models import User
from ninja.errors import HttpError
from django.utils.deprecation import MiddlewareMixin
from utils.cookie_deploy_handler import deploy_auth_cookie


log = logger()


class Auth_AccessAndSessionsMiddleware(MiddlewareMixin):
    def process_request(self, request):
        excluded_paths = [
            "/api/v1/auth/log-in",
            "/api/v1/auth/register",
        ]

        log.info("request path", path=request.path)

        if any(request.path.startswith(path) for path in excluded_paths):
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

        try:
            token = authorization.split(" ")[1]
        except (IndexError, AttributeError):
            return error_handler_400("Invalid authorization header format")

        if not email or not authorization:
            log.error(
                "Request header data missing", email=email, has_authorization=bool(authorization)
            )
            return error_handler_400("Email, and authorization must be provided on request header")

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

        # ==================================================================================
        # Since the session is still valid(i.e. the above check is passed), proceed with middleware to
        # check for access_token status - and renew all tokens/access for the user.
        #
        # The extra check for access_token expiration might seem needless since the session is still active, but
        # knowing the access_token status is helpful, as that can assist with triggering any relevant action and
        # track relevant data - if the token is expired.
        # ===================================================================================
        try:
            jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            # jwt_payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            # log.info("access_token jwt_payload", jwt_payload__access=jwt_payload)

            session_status = (
                f"ACTIVE ACCESS WITH ACTIVE SESSION: access and session renewed for '{email}'"
            )
            log.info("session_status", session_status=session_status)

        except jwt.ExpiredSignatureError:
            log.error("Token expired", token=token[:10] + "...")

            session_status = (
                f"ACTIVE SESSION WITH EXPIRED ACCESS: access and session renewed for '{email}'"
            )
            log.info("session_status", session_status=session_status)

            # ==================================================================================
            # Goal is not to terminate the function. Simply proceed and pass the request to the
            # view controller, since the session is still valid.
            # ==================================================================================

        except jwt.InvalidTokenError:
            log.error("Invalid token", token=token[:10] + "...")
            return error_handler_401("access denied - invalid token")

        tokens = generate_tokens({"user_id": user.id, "email": user.email, "token_type": "auth"})
        request.new_access_token = tokens.get('access_token')
        request.new_refresh_token = tokens.get('refresh_token')
        request.auth_cookie = tokens.get('auth_cookie')
        request.user = user

        return None  # continue processing

    def process_response(self, request, response):
        if hasattr(request, "auth_cookie"):
            # response.set_cookie("Fast_Django_Backend_Template", request.auth_cookie)

            # Deploy auth cookie
            deploy_auth_cookie({"response": response, "auth_cookie": request.auth_cookie})

        return response
