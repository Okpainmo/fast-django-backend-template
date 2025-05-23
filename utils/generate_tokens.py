import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from datetime import datetime, timedelta, timezone
from django.conf import settings
from django.contrib.auth.hashers import make_password, check_password
from utils.coded_error_handlers import error_handler_401
from utils.logger import logger

log = logger()


def generate_tokens(data):
    """
    Generate JWT tokens for authentication or one-time password purposes.

    This function can generate two types of tokens:
    1. Authentication tokens (access token, refresh token, and auth cookie)
    2. One-time password token

    Args:
        data (dict): A dictionary containing:
            - user_id: The user's unique identifier
            - email: The user's email address
            - token_type: Either "auth" for authentication tokens or "one_time_password" for OTP

    Returns:
        dict or str: For auth tokens, returns a dictionary containing:
            - auth_cookie: A secure cookie string
            - access_token: Short-lived JWT token (default 60 mins)
            - refresh_token: Long-lived JWT token (default 24 hrs)
        For one-time password, returns a JWT token string (default 5 mins lifetime)

    Raises:
        ValueError: If required attributes (user_id, email, token_type) are missing
        RuntimeError: If token generation fails due to an unforeseen error
    """
    access_expiry = int(settings.JWT_ACCESS_EXPIRATION_TIME)  # 60 mins(1 hr)
    session_expiry = int(settings.JWT_SESSION_EXPIRATION_TIME)  # 1440 mins(24hrs)
    one_time_password_expiry = int(settings.JWT_ONE_TIME_PASSWORD_LIFETIME)  # 5 minutes

    # log.info("access_expiry duration", access_expiry= int(settings.JWT_ACCESS_EXPIRATION_TIME)) # 60 mins(1 hr)
    # log.info("session_expiry duration", session_expiry= int(settings.JWT_SESSION_EXPIRATION_TIME)) # 60 mins(1 hr)
    # log.info("one_time_password_expiry duration", one_time_password_expiry= int(settings.JWT_ONE_TIME_PASSWORD_LIFETIME)) # 60 mins(1 hr)

    try:
        if not data.get('user_id') or not data.get('email'):
            raise ValueError("Data must contain 'user_id' and 'email' attributes.")

        if not data.get("token_type"):
            raise ValueError("Data must contain 'token_type' attribute.")

        if data.get("token_type") == "auth":
            access_expiration_time = datetime.now(timezone.utc) + timedelta(minutes=access_expiry)
            session_expiration_time = datetime.now(timezone.utc) + timedelta(minutes=session_expiry)

            access_token_payload_data = {
                "user_id": data.get('user_id'),
                "email": data.get('email'),
                "exp": access_expiration_time,  # Token expiration
                "iat": datetime.now(timezone.utc),  # Issued at time
            }

            refresh_token_payload_data = {
                "user_id": data.get('user_id'),
                "email": data.get('email'),
                "exp": session_expiration_time,  # Token expiration
                "iat": datetime.now(timezone.utc),  # Issued at time
            }

            # Encode the token
            access_token = jwt.encode(
                access_token_payload_data, settings.SECRET_KEY, algorithm="HS256"
            )
            refresh_token = jwt.encode(
                refresh_token_payload_data, settings.SECRET_KEY, algorithm="HS256"
            )

            auth_cookie_part_A = make_password(data.get('email'))
            auth_cookie_part_B = settings.SECRET_KEY

            auth_cookie = (
                f"Fast_Django_Backend_Template_____{auth_cookie_part_A}_____{auth_cookie_part_B}"
            )

            tokens = {
                "auth_cookie": auth_cookie,
                "access_token": access_token,
                "refresh_token": refresh_token,
            }

            # log.info("auth tokens inside generate tokens", tokens=tokens)

            return tokens

        if data.get("token_type") == "one_time_password":
            one_time_password_expiration_time = datetime.now(timezone.utc) + timedelta(
                minutes=one_time_password_expiry
            )  # 5 minutes

            one_time_password_payload_data = {
                "user_id": data.get('user_id'),
                "email": data.get('email'),
                "exp": one_time_password_expiration_time,  # Token expiration
                "iat": datetime.now(timezone.utc),  # Issued at time
            }

            one_time_password_token = jwt.encode(
                one_time_password_payload_data, settings.SECRET_KEY, algorithm="HS256"
            )

            # log.info("one time password token", token=one_time_password_token)
            return one_time_password_token

    except ExpiredSignatureError:
        return error_handler_401("access denied - access token is expired")
    except InvalidTokenError:
        return error_handler_401("access denied - invalid token")
