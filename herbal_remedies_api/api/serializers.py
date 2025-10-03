from rest_framework import serializers
from .models import Herb


class HerbSerializer(serializers.ModelSerializer):
  class Meta:
    model = Herb
    fields = ['id','name','category','description','uses','precautions']