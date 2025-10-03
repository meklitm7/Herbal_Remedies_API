from django.shortcuts import render
from rest_framework import generics
from .models import Herb
from .serializers import HerbSerializer

# Create your views here.
class HerbListCreateView(generics.ListCreateAPIView):
    queryset = Herb.objects.all()
    serializer_class = HerbSerializer

class HerbDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Herb.objects.all()
    serializer_class = HerbSerializer
