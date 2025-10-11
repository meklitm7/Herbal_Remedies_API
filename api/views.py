from django.shortcuts import render
from rest_framework import generics, permissions, filters, parsers
from django.db.models import Q
from .models import Herb
from .serializers import HerbSerializer

# Create your views here.
class HerbListCreateView(generics.ListCreateAPIView):
    queryset = Herb.objects.all()
    serializer_class = HerbSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'category', 'uses']

    parser_classes = [parsers.MultiPartParser, parsers.FormParser]

    def get_queryset(self):
        queryset = super().get_queryset()

        # Get multiple ailments (e.g., ?ailment=headache&ailment=fever)
        ailments = self.request.query_params.getlist('ailment')
        if ailments:
            ailment_queries = Q()
            for ailment in ailments:
                ailment_queries |= Q(ailments__icontains=ailment)
            queryset = queryset.filter(ailment_queries)

        return queryset

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    # Pass request context for full image URLs
    def get_serializer_context(self):
        return {'request': self.request}

class HerbDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Herb.objects.all()
    serializer_class = HerbSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]

    # Pass request context for full image URLs
    def get_serializer_context(self):
        return {'request': self.request}

    def update(self, request, *args, **kwargs):
        if request.method == 'PATCH':
            return super().partial_update(request, *args, **kwargs)
        return super().update(request, *args, **kwargs)


