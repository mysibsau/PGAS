from django.urls import path

from . import views

app_name = "statement"

urlpatterns = [
    path("", views.StatementListView.as_view(), name="list"),
    path("new/", views.StatementCreateView.as_view(), name="creat"),
    path("rating", views.RatingListView.as_view(), name="rating"),
    path("<uuid:pk>/", views.StatementDetailView.as_view(), name="detail"),
]
