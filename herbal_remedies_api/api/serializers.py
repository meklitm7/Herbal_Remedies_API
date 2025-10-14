from rest_framework import serializers
from .models import Herb, Collection


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
class HerbForCollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Herb
        fields = ['id', 'name']

class CollectionSerializer(serializers.ModelSerializer):
    herbs = HerbForCollectionSerializer(many=True, read_only=True)
    herb_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False
    )

    class Meta:
        model = Collection
        fields = ['id', 'user', 'name', 'description', 'herbs', 'herb_ids', 'created_at']
        read_only_fields = ['user', 'created_at']

    def create(self, validated_data):
        herb_ids = validated_data.pop('herb_ids', [])
        collection = Collection.objects.create(**validated_data)
        for herb_id in herb_ids:
            try:
                herb = Herb.objects.get(id=herb_id, created_by=self.context['request'].user)
                collection.herbs.add(herb)
            except Herb.DoesNotExist:
                pass  # Skip invalid herb IDs
        return collection
    def update(self, instance, validated_data):
        herb_ids = validated_data.pop('herb_ids', None)
        instance = super().update(instance, validated_data)
        if herb_ids is not None:
            instance.herbs.clear()
            for herb_id in herb_ids:
                try:
                    herb = Herb.objects.get(id=herb_id, created_by=self.context['request'].user)
                    instance.herbs.add(herb)
                except Herb.DoesNotExist:
                    pass  # Skip invalid herb IDs
        return instance