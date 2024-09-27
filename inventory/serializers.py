from rest_framework import serializers
from .models import Item

class ItemSerializer(serializers.ModelSerializer):
    name = serializers.CharField(
        max_length=255,
        required=True,
        allow_blank=False
    )
    
    description = serializers.CharField(
        min_length=10,
        required=False,
        allow_blank=True
    )

    quantity = serializers.IntegerField(
        required=True,
        min_value=0
    )

    class Meta:
        model = Item
        fields = ['id', 'name', 'description', 'quantity', 'created_at', 'updated_at']
