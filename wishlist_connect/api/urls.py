from django.urls import path
from .views import (
    GiftListCreateView, GiftDetailView,
    WishlistDetailView, AnotherUserWishlistDetailView,
    GiftCopyListCreateView, GiftCopyDetailView,
    home
)

urlpatterns = [
    path('gifts/', GiftListCreateView.as_view(), name='gift-list-create'),
    path('gifts/<int:pk>/', GiftDetailView.as_view(), name='gift-detail'),
    path('gift-copies/', GiftCopyListCreateView.as_view(), name='gift-copy-list-create'),
    path('gift-copies/<int:pk>/', GiftCopyDetailView.as_view(), name='gift-copy-detail'),
    path('wishlist/<int:pk>', WishlistDetailView.as_view(), name='wishlist-detail'),
    path('another-wishlist/<int:user_id>/', AnotherUserWishlistDetailView.as_view(), name='another-user-wishlist-detail'),
    path('home/', home, name='home'),
]