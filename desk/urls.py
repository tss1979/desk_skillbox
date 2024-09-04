
from django.urls import path
from .views import PostsList, logout_view, sign_in_view, BaseRegisterView, like, dislike

urlpatterns = [
    path('', PostsList.as_view()),
    path('logout', logout_view),
    path('signin', sign_in_view),
    path('like/<int:pk>', like),
    path('dislike/<int:pk>', dislike),
    path('signup', BaseRegisterView.as_view(template_name='signup.html'), name='signup'),
]