from django.shortcuts import render
from rest_framework import generics, permissions, filters
from .models import Herb
from .serializers import HerbSerializer

# Create your views here.
class HerbListCreateView(generics.ListCreateAPIView):
    queryset = Herb.objects.all()
    serializer_class = HerbSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'category', 'uses']

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class HerbDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Herb.objects.all()
    serializer_class = HerbSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
