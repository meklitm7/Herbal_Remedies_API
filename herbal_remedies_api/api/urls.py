from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import HerbListCreateView, HerbDetailView, CollectionViewSet

router = DefaultRouter()
router.register(r'collections', CollectionViewSet, basename='collections')

urlpatterns = [
  path('herbs/', HerbListCreateView.as_view(), name='herb-list'),
  path('herbs/<int:pk>/', HerbDetailView.as_view(), name='herb-detail'),
  path('', include(router.urls)),
]