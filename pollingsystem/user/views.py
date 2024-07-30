from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import login, logout
from user.services import UserService
from utils.logger import logger
from pollingsystem.common import ServiceError, ResponseData
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from utils.docs_common import generate_response_schema, generate_schema_401


class SignIn(APIView):
    """
    Signin using credentials
    """

    @swagger_auto_schema(
        operation_description="Signin using credentials(e-mail and password)",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['email', 'password'],
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING, description="Email of user"),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description="Password of user")
            }
        ),
        responses={
            200: openapi.Response(description="Login successfully!",
                                  schema=generate_response_schema(errors=False, data=openapi.Schema(type=openapi.TYPE_OBJECT, properties={
                                      "user": openapi.Schema(type=openapi.TYPE_INTEGER, example=10)
                                  }))
                                  ),
            400: openapi.Response(description="Input validation error",
                                  schema=generate_response_schema(
                                      success=False)

                                  ),
            401: openapi.Response(description="Invalid login credentials",
                                  schema=generate_response_schema(
                                      success=False)
                                  )
        }
    )
    def post(self, request):
        data = request.data
        email = data.get("email")
        password = data.get("password")

        try:
            user = UserService.signin(data)
            if user:
                login(request=request, user=user)
                logger.info("User logged in", extra={
                            "email": email, "password": password})
                return Response(data=ResponseData(message="Login successfully!", data={"user": user.id}).to_dict())

            logger.info("User tried to login with wrong credentials",
                        extra={"email": email, "password": password})

            return Response(ResponseData(success=False, message="Incorrect email or password").to_dict())

        except ServiceError as e:
            return Response(e.data.to_dict(), status=e.status_code)


class SignUp(APIView):
    """
    Create user account.
    """

    @swagger_auto_schema(
        operation_description="Create user account",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['email', 'username', 'password',
                      'first_name', 'last_name'],
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING, description="The email address of the user"),
                'username': openapi.Schema(type=openapi.TYPE_STRING, description="The username chosen by the user"),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description="The password chosen by the user"),
                'first_name': openapi.Schema(type=openapi.TYPE_STRING, description="The first name of the user"),
                'last_name': openapi.Schema(type=openapi.TYPE_STRING, description="The last name of the user"),
            }
        ),
        responses={
            200: openapi.Response(description="Account created successfully!",
                                  schema=generate_response_schema(errors=False)
                                  ),
            400: openapi.Response(description="Input validation error",
                                  schema=generate_response_schema(
                                      success=False)

                                  )
        }
    )
    def post(self, request):
        data = request.data

        try:
            user = UserService.signup(data)
            logger.info("A new account is created", extra={"user": user.id})
            return Response(ResponseData(message="Account created successfully!").to_dict())

        except ServiceError as e:
            return Response(e.data.to_dict(), status=e.status_code)


class LogOut(APIView):
    """
    Logout the current authenticated user
    """

    @swagger_auto_schema(
        operation_description="Logout the current authenticated user",
        responses={
            200: openapi.Response(description="Logged out successfully!",
                                  schema=generate_response_schema(errors=False)
                                  ),
            401: openapi.Response(description="User is not logged in",
                                  schema=generate_response_schema(
                                      success=False, errors=False)
                                  )
        }
    )
    def post(self, request):
        if request.user.is_anonymous:
            return Response(ResponseData(success=False, message="You are not logged in").to_dict())

        logger.info("User is logged out", extra={"user": request.user.id})
        logout(request=request)
        return Response(ResponseData(message="Logged out successfully!").to_dict())


class Session(APIView):
    """
    Get details of user session. i.e., if user is authenticated or not
    """

    @swagger_auto_schema(
        operation_description="Get details of user session",
        responses={
            200: openapi.Response(description="User is authenticated",
                                  schema=openapi.Schema(type=openapi.TYPE_OBJECT, properties={
                                      'user': openapi.Schema(type=openapi.TYPE_INTEGER, example=100, description="ID of the user")
                                  })
                                  ),
            401: openapi.Response(description="User is not authenticated",
                                  schema=openapi.Schema(
                                      type=openapi.TYPE_OBJECT)
                                  )
        }
    )
    def get(self, request):
        if request.user.is_authenticated:
            return Response({"user": request.user.id})

        return Response({}, status=401)


class UserProfile(APIView):
    """Get authenticated user profile detail"""

    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Get profile details of authenticated user",
        responses={
            200: openapi.Response(description="Profile details",
                                  schema=generate_response_schema(errors=False, data=openapi.Schema(
                                      type=openapi.TYPE_OBJECT,
                                      properties={
                                          'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                                          'email': openapi.Schema(type=openapi.TYPE_STRING),
                                          'username': openapi.Schema(type=openapi.TYPE_STRING),
                                          'first_name': openapi.Schema(type=openapi.TYPE_STRING),
                                          'last_name': openapi.Schema(type=openapi.TYPE_STRING),
                                          'polls': openapi.Schema(type=openapi.TYPE_ARRAY, nullable=True, items=openapi.Schema(type=openapi.TYPE_OBJECT, properties={
                                              "id": openapi.Schema(type=openapi.TYPE_INTEGER),
                                              "title": openapi.Schema(type=openapi.TYPE_STRING, example="Pakistan Vs. India"),
                                          })),
                                      }

                                  ))),
            403: generate_schema_401()
        }
    )
    def get(self, requset):
        user = requset.user

        data = UserService.user_profile(user=user)

        return Response(ResponseData(data=data).to_dict())
