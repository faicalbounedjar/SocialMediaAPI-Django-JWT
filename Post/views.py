from django.shortcuts import get_object_or_404,render
from  rest_framework.decorators import api_view,permission_classes
from .models import Post,Comment
from rest_framework.pagination import PageNumberPagination
from django.contrib.auth.models import User
from .serializers import PostSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

# Create your views here.

# Post

@api_view(['GET'])
def get_all_posts(request):
    posts = Post.objects.all()
    serializer = PostSerializer(posts,many=True)
    return Response({'posts':serializer.data})

@api_view(['GET'])
def get_post_by_id(request,pk):
    post = get_object_or_404(Post,id=pk)
    serializer = PostSerializer(post,many=False)
    return Response({'posts':serializer.data})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_post(request):
    data =  request.data
    serializer = PostSerializer(data = data)
    if serializer.is_valid():
        post = Post.objects.create(
            **data,
            user=request.user
        )
        res = PostSerializer(post,many=False)
        return Response({'Post':res.data})
    else : 
        return Response(serializer.errors)
   
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_post(request,pk):
    post = get_object_or_404(Post, pk=pk)
    if post.user != request.user :
        return Response({"Error": "Invalid , You cannot update this post"})
    post.content = request.data['content']
    post.save()
    serializer = PostSerializer(post,many=False)
    return Response({"Post updated":serializer.data})

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_post(request,pk):
    post = get_object_or_404(Post, pk=pk)
    if post.user != request.user :
        return Response({"Error": "Invalid , You cannot delete this post"})
    post.delete()
    return Response({"details":'post deleted successfully'})

@api_view(['GET'])
def get_all_comments(request,pk):
    post = get_object_or_404(Post,id=pk)
    serializer = PostSerializer(post,many=False)
    return Response({'comments':serializer.data['comments']})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def new_comments(request,pk):
    user = request.user
    data = request.data 
    post = get_object_or_404(Post,id=pk)
    comment = post.comments.filter(user=user)
    if comment.exists():
        Comment.objects.create(
            user=user
            ,post=post,
            comment=data['comment']
        )
        return Response({'details':'comment added'})
    else : 
        Comment.objects.create(
            user=user
            ,post=post,
            comment=data['comment']
        )
        post.save()
        return Response({'details':'1st Comment added'})
    
@api_view(['Delete'])
@permission_classes([IsAuthenticated])
def delete_comment(request,post_id,comment_id):
    user = request.user
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return Response({'details': 'Post not found.'}, status=status.HTTP_404_NOT_FOUND)
    try:
        comment = Comment.objects.get(id=comment_id, user=user, post=post)
    except Comment.DoesNotExist:
        return Response({'details': 'Comment not found or you do not have permission to delete it.'}, status=status.HTTP_404_NOT_FOUND)
    comment.delete()
    return Response({'details': 'Comment deleted'}, status=status.HTTP_204_NO_CONTENT)


