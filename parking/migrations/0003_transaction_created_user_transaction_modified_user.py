# Generated by Django 4.2.10 on 2024-02-08 04:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('parking', '0002_transaction'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='created_user',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='created_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='transaction',
            name='modified_user',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='modified_user', to=settings.AUTH_USER_MODEL),
        ),
    ]