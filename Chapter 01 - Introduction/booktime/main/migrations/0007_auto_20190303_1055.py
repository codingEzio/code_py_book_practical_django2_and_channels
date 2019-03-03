# Generated by Django 2.1.7 on 2019-03-03 10:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_productname_capitalize_impl'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='producttag',
            name='products',
        ),
        migrations.AddField(
            model_name='product',
            name='tags',
            field=models.ManyToManyField(blank=True, to='main.ProductTag'),
        ),
    ]