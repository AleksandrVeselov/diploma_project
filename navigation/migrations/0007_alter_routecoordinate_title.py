# Generated by Django 4.2.5 on 2023-09-22 13:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('navigation', '0006_routecoordinate_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='routecoordinate',
            name='title',
            field=models.CharField(max_length=50, verbose_name='Название точки'),
        ),
    ]