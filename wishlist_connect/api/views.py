from rest_framework import generics, permissions
from .models import Gift
from .forms import GiftForm
from .serializers import GiftSerializer
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.http import Http404
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

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

@login_required
def user_gift_list(request):
    gifts = Gift.objects.filter(user=request.user)
    return render(request, 'user_gift_list.html', {'gifts': gifts})

@login_required
def edit_gift(request, pk):
    gift = get_object_or_404(Gift, pk=pk, user=request.user)

    if request.method == 'POST':
        form = GiftForm(request.POST, instance=gift)
        if form.is_valid():
            form.save()
            return redirect('user-gift-list')
    else:
        form = GiftForm(instance=gift)

    return render(request, 'edit_gift.html', {'form': form, 'gift': gift})

@login_required
def other_user_gift_list(request, user_id):
    other_user = get_object_or_404(User, id=user_id)
    gifts = Gift.objects.filter(user=other_user)
    return render(request, 'other_user_gift_list.html', {'gifts': gifts, 'other_user': other_user})

def view_gift(request, pk):
    gift = get_object_or_404(Gift, pk=pk)
    return render(request, 'view_gift.html', {'gift': gift})

@login_required
def delete_selected_gifts(request):
    if request.method == 'POST':
        selected_gifts = request.POST.getlist('selected_gifts')
        Gift.objects.filter(pk__in=selected_gifts, user=request.user).delete()
    return redirect('user-gift-list')

@login_required
def delete_gift(request, pk):
    gift = get_object_or_404(Gift, pk=pk, user=request.user)
    gift.delete()
    return redirect('user-gift-list')

@login_required
def create_gift(request):
    if request.method == 'POST':
        form = GiftForm(request.POST)
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

def enter_user_id(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise Http404("User does not exist")

        return redirect('other-user-gift-list', user_id=user_id)

    return render(request, 'enter_user_id.html')
