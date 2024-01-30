from rest_framework import generics
from .models import Gift, Wishlist, CopyOfGift
from .serializers import GiftSerializer, WishlistSerializer, CopyOfGiftSerializer
from django.shortcuts import render

class GiftListCreateView(generics.ListCreateAPIView):
    queryset = Gift.objects.all()
    serializer_class = GiftSerializer

class GiftDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Gift.objects.all()
    serializer_class = GiftSerializer

class GiftCopyListCreateView(generics.ListCreateAPIView):
    queryset = CopyOfGift.objects.all()
    serializer_class = CopyOfGiftSerializer

class GiftCopyDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CopyOfGift.objects.all()
    serializer_class = CopyOfGiftSerializer

class WishlistDetailView(generics.RetrieveAPIView):
    queryset = Wishlist.objects.all()
    serializer_class = WishlistSerializer
    lookup_field = 'pk'

class AnotherUserWishlistDetailView(generics.RetrieveAPIView):
    queryset = Wishlist.objects.all()
    serializer_class = WishlistSerializer
    lookup_field = 'user__id'

def home(request):
    return render(request, 'home.html')