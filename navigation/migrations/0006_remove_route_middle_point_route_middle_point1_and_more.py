# Generated by Django 4.2.5 on 2023-09-17 13:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('navigation', '0005_route_middle_point'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='route',
            name='middle_point',
        ),
        migrations.AddField(
            model_name='route',
            name='middle_point1',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='middle_point1', to='navigation.routecoordinate', verbose_name='Промежуточная координата1'),
        ),
        migrations.AddField(
            model_name='route',
            name='middle_point2',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='middle_point2', to='navigation.routecoordinate', verbose_name='Промежуточная координата2'),
        ),
        migrations.AddField(
            model_name='route',
            name='middle_point3',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='middle_point3', to='navigation.routecoordinate', verbose_name='Промежуточная координата3'),
        ),
    ]
