from rest_framework import serializers
from .models import Gift, Wishlist

class GiftSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gift
        fields = '__all__'

class WishlistSerializer(serializers.ModelSerializer):
    gifts = GiftSerializer(many=True, read_only=True)

    class Meta:
        model = Wishlist
        fields = '__all__'