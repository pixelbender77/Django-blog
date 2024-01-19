from django.urls import path
from blog import views as blogViews

urlpatterns = [
    path('',blogViews.PostListView.as_view(),name='post_list'), 
    path('about/',blogViews.AboutView.as_view(),name='about' ),
    path('post/<int:pk>/',blogViews.PostDetailView.as_view(),name='post_detail'),
    path('post/new/',blogViews.CreatePostView.as_view(),name='post_new'),
    path('post/<int:pk>/edit/',blogViews.PostUpdateView.as_view(),name='post_edit'),
    path('post/<int:pk>/remove/',blogViews.PostDeleteView.as_view(),name='post_remove'),
    path('drafts/',blogViews.DraftListView.as_view(),name='post_draft_list'),
    path('post/<int:pk>/comment/',blogViews.add_comment_to_post,name='add_comment_to_post'),
    path('post/<int:pk>/like',blogViews.add_like_to_post,name='add_like_to_post'), # <-- added this myself :-b
    path('comment/<int:pk>/approve/',blogViews.comment_approve,name='comment_approve'),
    path('comment/<int:pk>/delete/',blogViews.comment_remove,name='comment_remove'),
    path('post/<int:pk>/publish/',blogViews.post_publish,name='post_publish'),

    
]
