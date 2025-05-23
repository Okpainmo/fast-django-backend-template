"""
Access Token Middleware for Django

This middleware handles access token validation and renewal for authenticated routes.
It works in conjunction with the session middleware to provide a complete authentication system.

The middleware performs the following checks:
1. Validates access tokens from the authorization header
2. Handles token expiration and renewal
3. Provides fresh access tokens for active sessions
4. Attaches user context to the request
5. Manages auth cookie deployment

Excluded paths:
- /api/v1/auth/log-in
- /api/v1/auth/register
- /, /api, /api/
"""

import jwt
from django.conf import settings
from utils.generate_tokens import generate_tokens
from utils.coded_error_handlers import error_handler_400, error_handler_401, error_handler_404
from utils.logger import logger
from domain__user.models import User
from django.utils.deprecation import MiddlewareMixin
from utils.cookie_deploy_handler import deploy_auth_cookie


log = logger()


class Auth_AccessMiddleware(MiddlewareMixin):
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
        # check for auth_cookie again here, just to be super-secure
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
        # Since the session is still valid(i.e. the previous(session) middleware is passed is passed),
        # proceed to check for access_token status - and renew all tokens/access for the user.
        #
        # The extra check for access_token expiration might seem needless since the session is still active
        # and we'll be renewing the access-token as a result, but knowing the access_token status is helpful, 
        # as that can assist with triggering any relevant action and to track relevant data - if the 
        # token is expired.
        # ===================================================================================
        try:
            token = authorization.split(" ")[1]
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
        
        # now proceed to check for the user
        user = User.objects.filter(email=email).first()

        if not user:
            log.error("User not found", email=email)
            return error_handler_404(f"User with email: '{email}' not found or does not exist.")

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
