from django.urls import path
from . import views

urlpatterns = [
    path('', views.api_root, name='api-root'), 
    # Authentication
    path('auth/register/', views.RegisterView.as_view(), name='register'),
    path('auth/login/', views.login_view, name='login'),
    path('auth/logout/', views.logout_view, name='logout'),
    
    # Profiles
    path('profiles/<int:id>/', views.ProfileDetailView.as_view(), name='profile-detail'),
    
    # Posts
    path('posts/', views.PostListView.as_view(), name='post-list'),
    path('posts/<int:pk>/', views.PostDetailView.as_view(), name='post-detail'),
    
    # Comments
    path('posts/<int:post_id>/comments/', views.CommentListView.as_view(), name='comment-list'),
    path('comments/<int:pk>/', views.CommentDetailView.as_view(), name='comment-detail'),
    
    # Likes
    path('posts/<int:post_id>/like/', views.post_like_view, name='post-like'),
    path('comments/<int:comment_id>/like/', views.comment_like_view, name='comment-like'),
    
    # Follow
    path('users/<int:user_id>/follow/', views.follow_user, name='follow-user'),
    
    # Search
    path('search/users/', views.search_users, name='user-search'),
    
    # News Feed
    path('feed/', views.news_feed, name='news-feed'),
]