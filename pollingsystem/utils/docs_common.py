"""This module provides methods for generating common API documentation schemas."""


from drf_yasg import openapi


def generate_response_schema(success=True, data=None, errors=True):
    """Generate API response schema

    Args:
        success (bool, optional): Success of response . Defaults to True.
        data (openapi.Schema, optional): Schema of data field. Defaults to None.

    Returns:
        openapi.Schema: Schema for API response
    """

    schema = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'success': openapi.Schema(
                type=openapi.TYPE_BOOLEAN,
                description="Indicates if the request was successful. Always `true`." if success else "Indicates if the request was successful. Always `false`."
            ),
            'message': openapi.Schema(
                type=openapi.TYPE_STRING,
                description="A message providing additional information about the response."
            ),
            'data': openapi.Schema(
                type=openapi.TYPE_OBJECT,
                example=None,
                default=None,
                description="Requested data. Always `null`."
            ) if data is None else data,

            'errors': openapi.Schema(
                type=openapi.TYPE_OBJECT,
                description="Error messages for input fields. Each key corresponds to a input field name." if errors else "Error messages for input fields. Each key corresponds to the input field names. Always `null`.",
                additional_properties=openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_STRING,
                        example="This field is required"
                    )
                )
                if errors else None
            )
        })

    return schema


def generate_schema_401():

    schema = openapi.Response(description="User is not authenticated", schema=openapi.Schema(type=openapi.TYPE_OBJECT, properties={
        'detail': openapi.Schema(type=openapi.TYPE_STRING, default="Authentication credentials were not provided.")
    }))

    return schema
