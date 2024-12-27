from django.urls import path
from .views import *


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('user/', UserProfileViewSet.as_view({'get': 'list'}), name='user'),
    path('post/', PostListAPIView.as_view(), name='post'),
    path('post/<int:pk>/', PostDetailAPIView.as_view(), name='post_detail'),
    path('post_like/', PostLikeView.as_view(), name='post_like'),
    path('comment_like/', CommentLikeView.as_view(), name='comment_like'),
    path('comment/', CommentAPIView.as_view(), name='comment'),
    path('story/', StoryAPIView.as_view(), name='story'),
    path('follow/', FollowViewSet.as_view({'get': 'list'}), name='follow'),
    path('save/', SaveViewSet.as_view({'get': 'list', 'post': 'create'}), name='save'),
    path('save_item/', SaveItemViewSet.as_view({'get': 'list', 'post': 'create'}), name='save_item'),
]