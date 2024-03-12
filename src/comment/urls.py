from django.urls import path

from .views import CommentCreateView, ListCommentsViews

app_name = "comments"

urlpatterns = [
    path('new/', CommentCreateView.as_view(), name='create_comment'),
    path('<uuid:pk>/share/', ListCommentsViews.as_view(), name='share'),
]
