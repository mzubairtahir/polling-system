from django.urls import path
from user.views import SignIn, SignUp, Session, LogOut, UserProfile

urlpatterns = [
    path('signup', SignUp.as_view(), name="signup"),
    path('signin', SignIn.as_view(), name="signin"),
    path('logout', LogOut.as_view(), name="logout"),
    path('session', Session.as_view(), name="session"),
    path('profile', UserProfile().as_view(), name="profile"),
]
