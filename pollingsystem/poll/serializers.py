from datetime import datetime
from rest_framework.fields import empty
from rest_framework.serializers import ModelSerializer, ValidationError, ImageField, SerializerMethodField, PrimaryKeyRelatedField
from poll.models import Poll, Vote, PollOption
from user.models import CustomUser
import base64
from django.core.files.base import ContentFile


class OptPictureSer(ImageField):
    """Serializer for handling poll option pictures, including base64 image encoding."""

    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            # Decode base64 encoded image data
            # Extract format and image string
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]  # Determine file extension

            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
            return super(OptPictureSer, self).to_internal_value(data)

        raise ValidationError("Image data is not in base64 format")


class PollOptionSerializer(ModelSerializer):
    """Serializer for poll options, including handling of associated pictures and vote counts."""

    picture = OptPictureSer()  # Serializer for the poll option's picture
    total_votes = SerializerMethodField()  # Method field to calculate total votes

    class Meta:
        model = PollOption
        # Include these fields in the serialized output
        fields = ["id", "name", "picture", "total_votes"]

    def get_total_votes(self, obj):
        """Return the total number of votes for this poll option."""
        return obj.votes.count()


class UserSerializer(ModelSerializer):
    """Serializer for user data."""

    class Meta:
        model = CustomUser
        # Include user ID and username in the serialized output
        fields = ["id", "username"]


class PollSerializer(ModelSerializer):
    """Serializer for poll data, with validation and voting status checks."""

    # Read-only serializer for the poll creator
    user = UserSerializer(read_only=True)
    user_id = PrimaryKeyRelatedField(
        queryset=CustomUser.objects.all(), source='user', write_only=True)

    # Serializer for the poll's options
    options = PollOptionSerializer(many=True)
    # Method field to check if the user has voted
    voted = SerializerMethodField(read_only=True)

    class Meta:
        model = Poll
        fields = '__all__'
        # Include all fields from the Poll model and the voted field
        extra_fields = ['voted', 'user_id']

    def get_voted(self, obj):
        """Check if the user has voted on this poll based on their IP address."""
        user_ip = self.context.get("user_ip")
        return obj.votes.filter(participant__ip_address=user_ip).exists()

    def to_internal_value(self, data):
        """Convert input data to internal format."""
        return super().to_internal_value(data)

    def validate(self, data):
        """Ensure that exactly 2 poll options are provided."""
        data = super().validate(data)
        if len(data.get("options")) != 2:
            raise ValidationError("Poll must have exactly 2 options")
        return data

    def create(self, validated_data):
        """Create a new poll and associated options."""
        options_data = validated_data.pop('options')
        poll = Poll.objects.create(**validated_data)
        for option_data in options_data:
            PollOption.objects.create(poll=poll, **option_data)
        return poll
