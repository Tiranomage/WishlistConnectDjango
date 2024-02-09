# Generated by Django 5.0.1 on 2024-02-09 09:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_gift_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='gift',
            name='status',
            field=models.CharField(choices=[('given', 'Given'), ('not given', 'Not given'), ('booked', 'Booked')], default='not given', max_length=10),
        ),
    ]
