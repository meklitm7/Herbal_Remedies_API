from django.urls import path
from .views import HerbListCreateView, HerbDetailView

urlpatterns = [
  path('herbs/', HerbListCreateView.as_view(), name='herb-list'),
    path('herbs/<int:pk>/', HerbDetailView.as_view(), name='herb-detail'),
]