# Generated by Django 5.0.1 on 2024-02-03 17:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_gift_price_delete_copyofgift'),
    ]

    operations = [
        migrations.AddField(
            model_name='gift',
            name='priority',
            field=models.CharField(choices=[('high', 'High'), ('medium', 'Medium'), ('low', 'Low'), ('none', 'None')], default='none', max_length=10),
        ),
    ]
