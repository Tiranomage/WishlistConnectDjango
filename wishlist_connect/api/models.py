from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Gift(models.Model):
    PRIORITY_CHOICES = [
        ('high', 'High'),
        ('medium', 'Medium'),
        ('low', 'Low'),
        ('none', 'None'),
    ]

    STATUS_CHOICES = [
        ('given', 'Given'),
        ('not given', 'Not given'),
        ('booked', 'Booked'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='none')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='not given')
    image = models.ImageField(upload_to='gift_images/', blank=True, null=True)


    def __str__(self):
        return self.title

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    visible = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username

class Wishlist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gifts = models.ManyToManyField(Gift)

@receiver(post_save, sender=User)
def create_wishlist(sender, instance, created, **kwargs):
    if created:
        Wishlist.objects.create(user=instance)