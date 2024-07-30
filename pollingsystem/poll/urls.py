from django.urls import path
from poll.views import CreatePoll, DeletePoll, PollDetail, RemoveVote, CastVote

urlpatterns = [
    path('new', CreatePoll.as_view(), name="new_poll"),
    path('detail', PollDetail.as_view(), name="poll_detail"),
    path('delete', DeletePoll.as_view(), name="delete_poll"),
    path('vote/add', CastVote.as_view(), name="add_vote"),
    path('vote/remove', RemoveVote.as_view(), name="remove_vote")
]
