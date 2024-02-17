from rest_framework import generics, permissions
from .models import Gift, UserProfile
from .forms import GiftForm, UserProfileForm, GiftFilterForm
from .serializers import GiftSerializer
from django.shortcuts import get_object_or_404, render, redirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.http import JsonResponse
from django.db.models import Func, Q
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
import json

class GiftListCreateView(generics.ListCreateAPIView):
    queryset = Gift.objects.all()
    serializer_class = GiftSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class GiftDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Gift.objects.all()
    serializer_class = GiftSerializer
    permission_classes = [permissions.IsAuthenticated]

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('main-menu')
    else:
        form = UserCreationForm()

    return render(request, 'register.html', {'form': form})

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_gift_list(request):
    gifts = Gift.objects.filter(user=request.user)
    serializer = GiftSerializer(gifts, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def other_user_gift_list(request, user_id):
    user = get_object_or_404(User, id=user_id)
    gifts = Gift.objects.filter(user=user)
    serializer = GiftSerializer(gifts, many=True)
    return Response(serializer.data)

@login_required
def main_menu(request):
    return render(request, 'main_menu.html')

def apply_filter_logic(user, filter_params):
    gifts = Gift.objects.filter(user=user)

    price_min = filter_params.get('price_min')
    price_max = filter_params.get('price_max')
    priority = filter_params.get('priority')
    status = filter_params.get('status')
    types = filter_params.get('types')

    if price_min:
        gifts = gifts.filter(price__gte=price_min)

    if price_max:
        gifts = gifts.filter(price__lte=price_max)

    if priority:
        gifts = gifts.filter(priority=priority)

    if status:
        gifts = gifts.filter(status=status)

    if types:
        gifts = gifts.filter(types=types)

    return gifts

def process_filter_request(request, filter_params):
    filter_params['price_min'] = request.POST.get('price_min')
    filter_params['price_max'] = request.POST.get('price_max')
    filter_params['priority'] = request.POST.get('priority')
    filter_params['status'] = request.POST.get('status')
    filter_params['types'] = request.POST.get('types')

    return filter_params

@login_required
def edit_gift(request, pk):
    gift = get_object_or_404(Gift, pk=pk, user=request.user)

    if request.method == 'POST':
        form = GiftForm(request.POST, request.FILES, instance=gift)
        if form.is_valid():
            form.save()
            return redirect('user-gift-list')
    else:
        form = GiftForm(instance=gift)

    return render(request, 'edit_gift.html', {'form': form, 'gift': gift})

@login_required
def user_gift_list(request):
    gifts = Gift.objects.filter(user=request.user)
    sort_options = {
        'priority': 'Priority',
        'title': 'Alphabetical',
        'price': 'Price',
        'status': 'Status',
        'types' : 'Types',
    }

    filter_params = request.session.get('filter_params', {})
    
    if request.method == 'POST':
        filter_params = process_filter_request(request, filter_params)

    gifts = apply_filter_logic(request.user, filter_params)

    sort_by = request.GET.get('sort_by', 'priority')
    order = request.GET.get('order', 'asc')
    search_query = request.GET.get('search_query')

    if search_query:
        gifts = gifts.filter(Q(title__icontains=search_query) | Q(description__icontains=search_query))

    if order == 'desc':
        gifts = gifts.order_by(f'-{sort_by}')
    else:
        gifts = gifts.order_by(sort_by)

    request.session['filter_params'] = filter_params

    context = {
        'gifts': gifts,
        'sort_by': sort_by,
        'order': order,
        'sort_options': sort_options,
        'search_query': search_query,
    }

    return render(request, 'user_gift_list.html', context)

@login_required
def other_user_gift_list(request, user_id):
    other_user = get_object_or_404(User, id=user_id)
    
    try:
        other_user_profile = UserProfile.objects.get(user=other_user)
    except UserProfile.DoesNotExist:
        return render(request, 'user_not_found_notification.html')

    other_user_profile = UserProfile.objects.get(user=other_user)

    if not other_user_profile.visible:
        return render(request, 'invisible_user_notification.html', {'other_user': other_user})

    sort_options = {
        'priority': 'Priority',
        'title': 'Alphabetical',
        'price': 'Price',
        'status': 'Status',
        'types' : 'Types',
    }

    filter_params = request.session.get('filter_params', {})
    
    if request.method == 'POST':
        filter_params = process_filter_request(request, filter_params)

    gifts = apply_filter_logic(request.user, filter_params)

    sort_by = request.GET.get('sort_by', 'priority')
    order = request.GET.get('order', 'asc')
    search_query = request.GET.get('search_query')

    if search_query:
        gifts = gifts.filter(Q(title__icontains=search_query) | Q(description__icontains=search_query))

    if order == 'desc':
        gifts = gifts.order_by(f'-{sort_by}')
    else:
        gifts = gifts.order_by(sort_by)

    request.session['filter_params'] = filter_params

    context = {
        'gifts': gifts,
        'sort_by': sort_by,
        'order': order,
        'sort_options': sort_options,
        'other_user': other_user,
        'other_user_profile': other_user_profile,
        'search_query': search_query,
    }

    return render(request, 'other_user_gift_list.html', context)

@login_required
def delete_gift(request, pk):
    gift = get_object_or_404(Gift, pk=pk, user=request.user)
    gift.delete()
    return redirect('user-gift-list')

@login_required
def create_gift(request):
    if request.method == 'POST':
        form = GiftForm(request.POST, request.FILES)
        if form.is_valid():
            new_gift = form.save(commit=False)
            new_gift.user = request.user
            new_gift.save()

            return redirect('user-gift-list')
    else:
        form = GiftForm()

    return render(request, 'create_gift.html', {'form': form})

def home(request):
    return render(request, 'home.html')

@login_required
def enter_user_id(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        if not User.objects.filter(id=user_id).exists():
            if request.headers.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
                return JsonResponse({'error': 'User not found'}, status=404)
            else:
                return render(request, 'user_not_found_notification.html')

        return redirect('other-user-gift-list', user_id=user_id)

    return render(request, 'enter_user_id.html')

@login_required
def user_profile(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('main-menu')
    else:
        form = UserProfileForm(instance=profile)

    return render(request, 'user_profile.html', {'form': form})

@login_required
def clear_filters(request):
    if request.method == 'POST':
        request.session.pop('filter_params', None)

        return JsonResponse({'gifts': []})