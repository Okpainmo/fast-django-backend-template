from datetime import timedelta
from utils.logger import logger

log = logger()
def deploy_auth_cookie(data):
    """
    Deploy an authentication cookie for user sessions.

    This function sets a secure authentication cookie after successful login/registration.
    The cookie is used to maintain user sessions and validate subsequent requests.

    Args:
        data (dict): A dictionary containing:
            - 'response' (HttpResponse): Django's response object
            - 'auth_cookie' (str): The authentication cookie value

    Returns:
        None

    Raises:
        KeyError: If required keys are missing
        ValueError: If auth_cookie is not a string

    Note:
        Security settings:
        - httponly=True: Prevents JavaScript access
        - secure=True: HTTPS only
        - samesite='Strict': CSRF protection
        - max_age=24 hours: Session duration
    """
    # log.info('Deploying auth cookie', data=data)

    if not isinstance(data.get('auth_cookie'), str):
        raise ValueError('auth_cookie must be a string')

    response = data.get("response")
    auth_cookie = data.get('auth_cookie')

    response.set_cookie(
        'Fast_Django_Backend_Template', auth_cookie,
        httponly=True,
        secure=True,
        samesite='Strict',
        max_age=timedelta(hours=24).total_seconds(),
    )
   