from django.shortcuts import render
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import generics, permissions, filters, parsers
from django.db.models import Q
from .models import Herb,  Collection
from .serializers import HerbSerializer, CollectionSerializer

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

     
class CollectionViewSet(viewsets.ModelViewSet):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def add_herb(self, request, pk=None):
        collection = self.get_object()
        herb_id = request.data.get('herb_id')
        if not herb_id:
            return Response({'detail': 'herb_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            herb = Herb.objects.get(id=herb_id, created_by=request.user)
        except Herb.DoesNotExist:
            return Response({'detail': 'Herb not found or not owned by you'}, status=status.HTTP_404_NOT_FOUND)
        if collection.herbs.filter(id=herb.id).exists():
            return Response({'detail': 'Herb already in collection'}, status=status.HTTP_400_BAD_REQUEST)
        collection.herbs.add(herb)
        return Response({'detail': f'Herb {herb.name} added to collection'}, status=status.HTTP_200_OK)

