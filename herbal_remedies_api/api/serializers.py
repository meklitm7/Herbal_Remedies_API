from rest_framework import serializers
from .models import Herb


class HerbSerializer(serializers.ModelSerializer):
  class Meta:
    model = Herb
    fields = ['id','name','category','description','uses','precautions','created_by']
  def validate(self, data):
        user = self.context['request'].user
        name = data.get('name')
        uses = data.get('uses')

        if Herb.objects.filter(name=name, uses=uses, created_by=user).exists():
            raise serializers.ValidationError(
                "This herb with the same use already exists. Please add a different use or edit the existing one."
            )
        return data