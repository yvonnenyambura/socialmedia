from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import get_object_or_404
from django.db.models import Q
from .models import User, Post, Comment, Like, CommentLike, Follow
from .serializers import (
    UserRegistrationSerializer, UserSerializer, PostSerializer, 
    CommentSerializer
)

@api_view(['GET'])
def api_root(request):
    return Response({
        'message': 'Social Media API',
        'endpoints': {
            'register': '/api/auth/register/',
            'login': '/api/auth/login/',
            'posts': '/api/posts/',
            'feed': '/api/feed/',
            'search': '/api/search/users/',
            'admin': '/admin/'
        }
    })

# Authentication
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')
    
    user = authenticate(username=username, password=password)
    if user:
        login(request, user)
        return Response(UserSerializer(user).data)
    return Response({'error': 'Invalid credentials'}, status=400)

@api_view(['POST'])
def logout_view(request):
    logout(request)
    return Response({'message': 'Logged out successfully'})

# Profiles
class ProfileDetailView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'id'

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

# Posts
class PostListView(generics.ListCreateAPIView):
    serializer_class = PostSerializer

    def get_queryset(self):
        if self.request.user.is_authenticated:
            following_ids = self.request.user.following.values_list('following_id', flat=True)
            following_ids = list(following_ids) + [self.request.user.id]
            return Post.objects.filter(user_id__in=following_ids)
        return Post.objects.none()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

# Comments
class CommentListView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        post_id = self.kwargs['post_id']
        return Comment.objects.filter(post_id=post_id)

    def perform_create(self, serializer):
        post = get_object_or_404(Post, id=self.kwargs['post_id'])
        serializer.save(user=self.request.user, post=post)

class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

# Likes
@api_view(['POST', 'DELETE'])
def post_like_view(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    if request.method == 'POST':
        like, created = Like.objects.get_or_create(user=request.user, post=post)
        if created:
            return Response({'message': 'Post liked'}, status=201)
        return Response({'error': 'Already liked'}, status=400)
    
    elif request.method == 'DELETE':
        Like.objects.filter(user=request.user, post=post).delete()
        return Response({'message': 'Post unliked'})

@api_view(['POST', 'DELETE'])
def comment_like_view(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    
    if request.method == 'POST':
        like, created = CommentLike.objects.get_or_create(user=request.user, comment=comment)
        if created:
            return Response({'message': 'Comment liked'}, status=201)
        return Response({'error': 'Already liked'}, status=400)
    
    elif request.method == 'DELETE':
        CommentLike.objects.filter(user=request.user, comment=comment).delete()
        return Response({'message': 'Comment unliked'})

# Follow
@api_view(['POST', 'DELETE'])
def follow_user(request, user_id):
    user_to_follow = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        if request.user == user_to_follow:
            return Response({'error': 'Cannot follow yourself'}, status=400)
        
        follow, created = Follow.objects.get_or_create(
            follower=request.user, 
            following=user_to_follow
        )
        if created:
            return Response({'message': f'Now following {user_to_follow.username}'}, status=201)
        return Response({'error': 'Already following'}, status=400)
    
    elif request.method == 'DELETE':
        Follow.objects.filter(follower=request.user, following=user_to_follow).delete()
        return Response({'message': f'Unfollowed {user_to_follow.username}'})

# Search
@api_view(['GET'])
def search_users(request):
    query = request.GET.get('query', '')
    if query:
        users = User.objects.filter(
            Q(username__icontains=query) | 
            Q(first_name__icontains=query) | 
            Q(last_name__icontains=query)
        )
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
    return Response([])

# News Feed
@api_view(['GET'])
def news_feed(request):
    if request.user.is_authenticated:
        following_ids = request.user.following.values_list('following_id', flat=True)
        following_ids = list(following_ids) + [request.user.id]
        posts = Post.objects.filter(user_id__in=following_ids)
        serializer = PostSerializer(posts, many=True, context={'request': request})
        return Response(serializer.data)
    return Response([])