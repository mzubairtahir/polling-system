from rest_framework.views import APIView
from utils.docs_common import generate_response_schema, generate_schema_401
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from poll.services import PollService, VoteService
from pollingsystem.common import ServiceError, ResponseData
from utils.logger import logger
import ipaddress


class CreatePoll(APIView):
    """
    Create a new poll
    """
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Create a new poll",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['title', 'expiry_date', 'options'],
            properties={
                'title': openapi.Schema(type=openapi.TYPE_STRING, description="Title of the poll"),
                'expiry_date': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE, description="Expiry date of the poll in ISO format (YYYY-MM-DD)"),
                'options': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'name': openapi.Schema(type=openapi.TYPE_STRING, description="Name of poll option"),
                            'Picture': openapi.Schema(type=openapi.TYPE_STRING, description="String containing base64 image")
                        }
                    )
                )
            }
        ),
        responses={
            200: openapi.Response(description="Poll is created successfully!",
                                  schema=generate_response_schema(errors=False)
                                  ),
            400: openapi.Response(description="Invalid input or validation error",
                                  schema=generate_response_schema(
                                      success=False)

                                  ),
            401: generate_schema_401()
        }
    )
    def post(self, request):
        data = request.data
        data.update({"user_id": request.user.id})

        try:
            poll = PollService.create(data=data)
            response_data = ResponseData(
                message="Poll is created successfully!", data={"id": poll.id})
            return Response(response_data.to_dict())

        except ServiceError as e:
            return Response(e.data.to_dict(), status=e.status_code)


class DeletePoll(APIView):
    """
    Delete a poll
    """

    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Delete a poll",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['id'],
            properties={
                'id': openapi.Schema(type=openapi.TYPE_INTEGER, description="Valid ID of the poll to be deleted")
            }
        ),
        responses={
            200: openapi.Response(description="Poll is successfully deleted!",
                                  schema=generate_response_schema(errors=False)
                                  ),
            400: openapi.Response(description="Invalid input or validation error",
                                  schema=generate_response_schema(
                                      success=False)
                                  ),
            401: generate_schema_401(),
            403: openapi.Response(description="Forbidden - User not authorized to delete the poll",
                                  schema=generate_response_schema(
                                      success=False, errors=False)

                                  ),
            404: openapi.Response(description="Not Found - Poll with given ID does not exist",
                                  schema=generate_response_schema(
                                      success=False, errors=False)

                                  )
        }
    )
    def post(self, request):
        data = request.data
        poll_id = data.get("id")

        if not isinstance(poll_id, int):
            response_data = ResponseData(
                success=False, message="Invalid poll Id is given")
            return Response(response_data.to_dict(), status=400)

        try:
            PollService.delete(request.user, id=poll_id)
            response_data = ResponseData(
                message="Poll is successfully deleted!")
            return Response(response_data.to_dict())

        except ServiceError as e:
            return Response(e.data.to_dict(), status=e.status_code)


class PollDetail(APIView):
    """
    Get detail of a poll
    """

    @swagger_auto_schema(
        operation_description="Get detail of a poll",
        manual_parameters=[
            openapi.Parameter(
                name='poll_id',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                required=True,
                description='ID of the poll'
            ),
        ],
        responses={
            200: openapi.Response(description="Poll details retrieved successfully!",
                                  schema=generate_response_schema(errors=False, data=openapi.Schema(
                                      type=openapi.TYPE_OBJECT,
                                      properties={
                                          "id": openapi.Schema(type=openapi.TYPE_INTEGER),
                                          "user": openapi.Schema(
                                              type=openapi.TYPE_OBJECT,
                                              properties={
                                                  "id": openapi.Schema(type=openapi.TYPE_INTEGER),
                                                  "username": openapi.Schema(type=openapi.TYPE_STRING)
                                              }
                                          ),
                                          "options": openapi.Schema(
                                              type=openapi.TYPE_ARRAY,
                                              items=openapi.Schema(
                                                  type=openapi.TYPE_OBJECT,
                                                  properties={
                                                      "id": openapi.Schema(type=openapi.TYPE_INTEGER),
                                                      "name": openapi.Schema(type=openapi.TYPE_STRING),
                                                      "picture": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_URI, example=r"/media/polloption/2024/07/%26d/temp_GX4q1xk.png"),
                                                      "total_votes": openapi.Schema(type=openapi.TYPE_INTEGER)
                                                  }
                                              )
                                          ),
                                          "voted": openapi.Schema(type=openapi.TYPE_BOOLEAN),
                                          "date_created": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME, example="2024-07-25T11:35:44.599276Z"),
                                          "title": openapi.Schema(type=openapi.TYPE_STRING),
                                          "expiry_date": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME)
                                      }
                                  )
                                  )
                                  ),
            400: openapi.Response(description="Bad Request - Invalid ID format",
                                  schema=generate_response_schema(
                                      success=False, errors=False)
                                  ),
            404: openapi.Response(description="Not Found - Poll with given ID does not exist",
                                  schema=generate_response_schema(
                                      success=False, errors=False)
                                  )
        }
    )
    def get(self, request):
        poll_id = request.query_params.get("poll_id", None)
        try:
            poll_id = int(poll_id)
        except ValueError:
            return Response(ResponseData(success=False, message="Invalid ID").to_dict(), status=400)

        try:
            data = PollService.poll_detail(
                id=poll_id, request_user_ip=request.META.get("REMOTE_ADDR", None))
            return Response(ResponseData(data=data).to_dict())
        except ServiceError as e:
            return Response(e.data.to_dict(), e.status_code)


class CastVote(APIView):
    """
    Cast a vote to a poll
    """

    @swagger_auto_schema(
        operation_description="Cast a vote to a poll",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['poll_id', 'option_id'],
            properties={
                'poll_id': openapi.Schema(type=openapi.TYPE_INTEGER, description="ID of the poll"),
                'option_id': openapi.Schema(type=openapi.TYPE_INTEGER, description="ID of the poll option")
            }
        ),
        responses={
            200: openapi.Response(description="Vote casted successfully!",
                                  schema=generate_response_schema(errors=False)

                                  ),
            400: openapi.Response(description="Bad Request - Invalid input",
                                  schema=generate_response_schema(
                                      success=False)
                                  ),
            404: openapi.Response(description="Not Found - Poll or poll option with given ID does not exist",
                                  schema=generate_response_schema(
                                      success=False, errors=False)
                                  ),
        }
    )
    def post(self, request):
        data = request.data
        user_ip = request.META.get("REMOTE_ADDR", None)
        poll_option_id = data.get("option_id")
        poll_id = data.get("poll_id")

        try:
            ipaddress.ip_address(user_ip)
        except ValueError:
            logger.info("Invalid IP address is trying to cast vote",
                        extra={"IP": user_ip})
            response_data = ResponseData(
                success=False, message="Invalid IP address.")
            return Response(response_data.to_dict(), status=400)

        if not isinstance(poll_option_id, int) or not isinstance(poll_id, int):
            response_data = ResponseData(
                success=False, message="Invalid option Id or poll Id.")
            return Response(response_data.to_dict(), status=400)

        user = request.user if request.user.is_authenticated else None

        try:
            VoteService.create(participant_ip=user_ip, poll_id=poll_id,
                               poll_option_id=poll_option_id, user=user)
            response_data = ResponseData(message="Vote casted!")
            return Response(response_data.to_dict())
        except ServiceError as e:
            return Response(e.data.to_dict(), status=e.status_code)


class RemoveVote(APIView):
    """
    Remove a vote from a voted poll
    """

    @swagger_auto_schema(
        operation_description="Remove a vote from a voted poll",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['poll_id'],
            properties={
                'poll_id': openapi.Schema(type=openapi.TYPE_INTEGER, description="ID of the poll")
            }
        ),
        responses={
            200: openapi.Response(description="Vote removed successfully!",
                                  schema=generate_response_schema(errors=False)
                                  ),
            400: openapi.Response(description="Bad Request - Invalid data type of poll id",
                                  schema=generate_response_schema(
                                      success=False)
                                  ),
            404: openapi.Response(description="Not Found - Vote you are trying to remove is not present!",
                                  schema=generate_response_schema(
                                      success=False, errors=False)
                                  )
        }
    )
    def post(self, request):
        data = request.data
        poll_id = data.get("poll_id")
        participant_ip = request.META.get("REMOTE_ADDR", None)

        if not isinstance(poll_id, int):
            response_data = ResponseData(
                success=False, message="Invalid data type of poll id")
            return Response(response_data.to_dict(), status=400)

        try:
            VoteService.delete(poll_id=poll_id, participant_ip=participant_ip)
            response_data = ResponseData(message="Vote removed!")
            return Response(response_data.to_dict())
        except ServiceError as e:
            return Response(e.data.to_dict(), status=e.status_code)
