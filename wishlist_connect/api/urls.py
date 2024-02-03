from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (GiftListCreateView, GiftDetailView, 
                    user_gift_list, other_user_gift_list, 
                    main_menu, edit_gift, view_gift, home,
                    delete_selected_gifts, create_gift,
                    enter_user_id, delete_gift, register_view, 
                    user_profile)

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', register_view, name='register'),
    path('user-profile/', user_profile, name='user-profile'),
    path('gifts/', GiftListCreateView.as_view(), name='gift-list-create'),
    path('gifts/<int:pk>/', GiftDetailView.as_view(), name='gift-detail'),
    path('user-gift-list/', user_gift_list, name='user-gift-list'),
    path('edit-gift/<int:pk>/', edit_gift, name='edit-gift'),
    path('main-menu/', main_menu, name='main-menu'),
    path('enter-user-id/', enter_user_id, name='enter-user-id'),
    path('other-user-gift-list/<int:user_id>/', other_user_gift_list, name='other-user-gift-list'),
    path('view-gift/<int:pk>/', view_gift, name='view-gift'),
    path('home/', home, name='home'),
    path('delete-selected-gifts/', delete_selected_gifts, name='delete-selected-gifts'),
    path('delete-gift/<int:pk>/', delete_gift, name='delete-gift'),
    path('create-gift/', create_gift, name='create-gift'),
]   
