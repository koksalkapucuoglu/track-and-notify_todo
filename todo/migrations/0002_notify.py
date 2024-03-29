# Generated by Django 3.2.13 on 2023-04-28 22:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('todo', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notify',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('minute', models.CharField(default='*', max_length=20)),
                ('hour', models.CharField(default='*', max_length=20)),
                ('day_of_week', models.CharField(default='*', max_length=20)),
                ('day_of_month', models.CharField(default='*', max_length=20)),
                ('month_of_year', models.CharField(default='*', max_length=20)),
                ('status', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='todo.status')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
