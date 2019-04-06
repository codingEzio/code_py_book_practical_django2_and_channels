# Generated by Django 2.1.7 on 2019-04-06 10:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_order_orderline'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='last_spoken_to',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='cs_chats', to='main.User'),
        ),
    ]
