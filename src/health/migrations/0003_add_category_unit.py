# Generated by Django 2.1.7 on 2019-03-16 04:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('health', '0002_index_add_desc'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='unit',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name='Category.unit'),
        ),
    ]
