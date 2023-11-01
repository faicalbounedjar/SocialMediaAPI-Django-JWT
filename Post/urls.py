from django.urls import path
from . import views

urlpatterns = [
    path('',views.get_all_posts,name='get_all_posts'),
    path('add/',views.add_post,name='add_post'),
    path('update/<str:pk>',views.update_post,name='update_post'),
    path('delete/<str:pk>',views.delete_post,name='delete_post'),
    path('<str:pk>/comments',views.new_comments,name='add_comment'),
    path('<str:post_id>/comments/<str:comment_id>/delete',views.delete_comment,name='delete_comment'),
    path('<str:pk>/all',views.get_all_comments,name='comment'),
]
