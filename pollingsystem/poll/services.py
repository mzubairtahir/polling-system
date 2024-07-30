"""This module contains services that can be used in views to interact with our models."""

from poll.serializers import PollSerializer
from poll.models import Poll, Vote, PollOption
from user.models import Participant
from pollingsystem.common import ServiceError, ResponseData
from utils.logger import logger


class PollService:

    @staticmethod
    def poll_detail(request_user_ip, id):
        """Get poll detail

        Args:
            id (int): Id of poll

        Returns:
            data: serialized data
        """

        required_poll = Poll.objects.filter(id=id)
        if required_poll.exists():
            poll_serializer = PollSerializer(required_poll.first(), context={
                                             "user_ip": request_user_ip})
            data = poll_serializer.data
            return data

        raise ServiceError(data=ResponseData(
            success=False, message="This poll is not available"), status_code=404)

    @staticmethod
    def create(data: dict):
        """Create new poll

        Args:
            data (dict): Data to create the poll
        Returns:
            Poll: new poll that is created
        """

        poll_serializer = PollSerializer(data=data)

        if poll_serializer.is_valid():
            poll = poll_serializer.save()
            logger.info("Poll created", extra={
                        "user": poll.user.id, "poll_id": poll.id})
            return poll

        errors = poll_serializer.errors
        raise ServiceError(data=ResponseData(
            success=False, message="Poll submission failed. Check your entries and try again.", errors=errors), status_code=400)

    @staticmethod
    def delete(user, id):
        """Delete a poll

        Args:
            user (CustomUser): User that is requesting to delete poll
            id (int): Id of the poll
        """

        try:
            poll = Poll.objects.get(id=id)
            if poll.user != user:
                logger.info("Unauthorized user is trying to deletea poll", extra={
                    "request_user": user.id, "poll_id": id, "poll_user": poll.user.id})

                raise ServiceError(data=ResponseData(
                    success=False, message="You are not authorized to delete this poll"), status_code=403)

            poll_id = poll.id
            poll.delete()

            logger.info("Poll id deleted", extra={
                        "user": user.id, "poll_id": poll_id})

        except Poll.DoesNotExist:
            raise ServiceError(data=ResponseData(
                success=False, message=f"Poll with id {id} does not exist"), status_code=404)


class VoteService:

    @staticmethod
    def create(participant_ip, poll_id, poll_option_id, user=None):
        """Create or cast a new vote

        Args:
            participant_ip (str): Ip address of the participant
            poll_id (int): Id of the poll
            poll_option_id (_type_): Id of the poll option that participant selected
            user (CustomUser, optional): object of user if user is participating. Defaults to None.
        """

        # check if previous vote exists
        vote = Vote.objects.filter(
            participant__ip_address=participant_ip, poll__id=poll_id)

        if vote.exists():
            # clear previous vote
            if not vote.first().poll_option.id == poll_option_id:
                vote.first().delete()

        poll = Poll.objects.filter(id=poll_id)
        poll_option = PollOption.objects.filter(id=poll_option_id)

        if not (poll.exists() and poll_option.exists()):
            # if given poll and poll option IDs are not present  in db

            message = "This poll does not exists!" if (
                not poll.exists()) else "This poll option does not exist"

            raise ServiceError(data=ResponseData(
                success=False, message=message), status_code=404)

        participant, _ = Participant.objects.get_or_create(
            # ip_address=participant_ip, user=user)
            ip_address=participant_ip)

        vote = Vote.objects.create(participant=participant,
                                   poll=poll.first(), poll_option=poll_option.first())

        vote.save()
        logger.info("Vote is casted", extra={
            "participant": participant_ip, "poll_id": poll_id, "option_id": poll_option_id})

    @staticmethod
    def delete(poll_id, participant_ip):

        try:
            vote = Vote.objects.get(
                participant__ip_address=participant_ip, poll=poll_id)
            vote.delete()

            logger.info("Vote is removed", extra={
                "participant": participant_ip, "poll_id": poll_id, "option_id": vote.poll_option.id})

        except Vote.DoesNotExist:
            raise ServiceError(data=ResponseData(
                success=False, message="Vote you are trying to remove is not present!"), status_code=404)
