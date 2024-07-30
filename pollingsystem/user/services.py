from user.serializers import LoginValidator, SignUpValidator, ProfileSerializer
from user.models import CustomUser
from pollingsystem.common import ServiceError, ResponseData
from django.contrib.auth import authenticate


class UserService:

    @staticmethod
    def signin(data: dict):
        """Get user object on base of email and password

        Args:
            data (dict): Data including email and password

        Returns:
            CustomUsre: User object
            None: If credentials are invalid
        """

        serializer = LoginValidator(data=data)
        if serializer.is_valid():
            email = serializer.validated_data.get("email")
            password = serializer.validated_data.get("password")
            user = authenticate(
                email=email, password=password)
            return user

        errors = serializer.errors
        raise ServiceError(data=ResponseData(
            success=False, message="Sign In failed. Check your entries and try again.", errors=errors), status_code=400)

    @staticmethod
    def signup(data):

        validator = SignUpValidator(data=data)
        if validator.is_valid():
            # user = validator.save()
            password = validator.validated_data.pop("password")
            user = CustomUser(**validator.validated_data)
            user.set_password(password)
            user.save()
            return user

        errors = validator.errors
        raise ServiceError(data=ResponseData(
            success=False, message="Sign Up failed. Check your entries and try again.", errors=errors), status_code=400)

    @staticmethod
    def user_profile( user):

        serializer = ProfileSerializer(user)
        return serializer.data
        # pass