from rest_framework import serializers
from .models import Herb


class HerbSerializer(serializers.ModelSerializer):
  image_url = serializers.SerializerMethodField() 
  class Meta:
    model = Herb
    fields = [
        'id',
        'name',
        'category',
        'other_category_explanation',
        'description',
        'uses',
        'ailments',
        'precautions',
        'image',
        'image_url',
        'created_by'
        ]
    read_only_fields = ['created_by']

  def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None
  
  def validate(self, data):
        user = self.context['request'].user
        name = data.get('name')
        uses = data.get('uses')
        category = data.get('category')
        explanation = data.get('other_category_explanation')

        herb_id = getattr(self.instance, 'id', None)

        if herb_id is None and Herb.objects.filter(name=name, uses=uses, created_by=user).exists():
            raise serializers.ValidationError(
                "This herb with the same use already exists. Please add a different use or edit the existing one."
            )
        # Ensure explanation is given when category is "Other"
        if category == 'other' and not explanation:
            raise serializers.ValidationError({
                "other_category_explanation": "Please explain the herb part when 'Other' is selected."
            })
        # Ensure explanation is NOT given for standard categories
        if category != 'other' and explanation:
            raise serializers.ValidationError({
                "other_category_explanation": "Explanation is only allowed when category is 'Other'."
            })

        return data