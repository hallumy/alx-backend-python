from rest_framework_simplejwt.authentication import JWTAuthentication

class CustomJWTAuthentication(JWTAuthentication):
    """
    You can extend this for custom user validation logic if needed.
    """
    pass
