# Generated by Django 4.2.5 on 2023-09-17 12:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('navigation', '0004_alter_routecoordinate_latitude_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='route',
            name='middle_point',
            field=models.ManyToManyField(blank=True, null=True, related_name='middle_point', to='navigation.routecoordinate', verbose_name='Промежуточная координата'),
        ),
    ]
