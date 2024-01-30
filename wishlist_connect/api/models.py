from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Gift(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    
class CopyOfGift(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    original_gift = models.ForeignKey(Gift, on_delete=models.CASCADE)

class Wishlist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gifts = models.ManyToManyField(Gift)

@receiver(post_save, sender=User)
def create_wishlist(sender, instance, created, **kwargs):
    if created:
        Wishlist.objects.create(user=instance)