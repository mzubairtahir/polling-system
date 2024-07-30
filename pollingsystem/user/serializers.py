from rest_framework.serializers import ModelSerializer, EmailField, Serializer, CharField
from poll.models import Poll
from user.models import CustomUser

class LoginValidator(Serializer):
    """Serializer for validating user login credentials."""

    email = CharField()  # User's email address.
    password = CharField()  # User's password.

class SignUpValidator(ModelSerializer):
    """Serializer for validating user signup data."""

    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'password', 'first_name', 'last_name']  # Fields required for user registration.

class PollSerializer(ModelSerializer):
    """Serializer for representing Poll data."""

    class Meta:
        model = Poll
        fields = ["id", "title"]  # Fields for Poll model.

class ProfileSerializer(ModelSerializer):
    """Serializer for serializing user profile data."""

    polls = PollSerializer(read_only=True, many=True)  # Serialized list of polls associated with the user.

    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'first_name', 'last_name', "polls"]  # Fields for CustomUser model including associated polls.
