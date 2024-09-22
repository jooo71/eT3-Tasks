# Generated by Django 5.1.1 on 2024-09-22 11:51

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transctions', '0021_alter_transaction_recipient_alter_transaction_sender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='recipient',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='received_transactions', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='sender',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='sent_transactions', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
