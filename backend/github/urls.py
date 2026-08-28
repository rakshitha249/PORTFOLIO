from django.urls import path
from .views import RepositoryListView

urlpatterns = [
    path('repositories/', RepositoryListView.as_view(), name='github-repositories'),
]
