from django.urls import path
from . import views 

app_name = 'posts'

urlpatterns = [
    path('',views.PostListView.as_view(),name='all'),
    path('new/',views.CreatePost.as_view(),name='create'),
    path('by/<username>',views.UserPost.as_view(),name='for_user'),
    path('by/<username>/<int:pk>',views.PostDetail.as_view(),name='post_detail'),
    path('delete/<int:pk>',views.DeletPost.as_view(),name='delete'),
    path('posts/<int:pk>/comment',views.add_comment_to_post,name='add_comment_post'),
    path('comment/<int:pk>/approve',views.comment_approve,name='commet_approve'),
    path('comment/<int:pk>/remove',views.comment_remove,name='comment_remove'),
    
    
]
