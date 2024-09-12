
from django.urls import path
from .views import PostsList, logout_view, sign_in_view, BaseRegisterView, like_view, dislike_view, \
    send_message_view, PostsListSearch, PostDetail, PostUpdate, PostDelete, PostCreate, \
    subscribe, delete_comment, sign_in_with_code_view, confirm_comment, CommentListSearch

urlpatterns = [
    path('', PostsList.as_view()),
    path('<int:pk>', PostDetail.as_view(), name='detail'),
    path('create', PostCreate.as_view(), name='create'),
    path('edit/<int:pk>', PostUpdate.as_view(), name='edit'),
    path('delete/<int:pk>', PostDelete.as_view(), name='delete'),
    path('delete_comment/<int:pk>', delete_comment, name='delete_comment'),
    path('confirm_comment/<int:pk>', confirm_comment, name='confirm_comment'),
    path('comments', CommentListSearch.as_view(), name='comments'),
    path('logout', logout_view),
    path('signin', sign_in_view),
    path('signin_code', sign_in_with_code_view, name='sign_code'),
    path('like/<int:pk>', like_view, name='like'),
    path('dislike/<int:pk>', dislike_view, name='dislike'),
    path('send_message/<int:pk>', send_message_view, name='send_message'),
    path('signup', BaseRegisterView.as_view(template_name='signup.html'), name='signup'),
    path('search', PostsListSearch.as_view(), name='search'),
    path('subscribe', subscribe, name='subscribe'),
]