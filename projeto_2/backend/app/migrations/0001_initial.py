# Generated by Django 5.0 on 2023-12-21 16:25

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('price', models.FloatField(max_length=100)),
                ('max_guests', models.IntegerField()),
                ('image', models.ImageField(blank=True, default=None, null=True, upload_to='images/')),
                ('type', models.CharField(choices=[('d', 'Double'), ('t', 'Triple'), ('q', 'Quad'), ('s', 'Suite')], default='d', max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_price', models.DecimalField(decimal_places=2, max_digits=100)),
                ('check_in', models.DateField()),
                ('check_out', models.DateField()),
                ('breakfast', models.BooleanField(default=False)),
                ('lunch', models.BooleanField(default=False)),
                ('extra_bed', models.BooleanField(default=False)),
                ('room_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.room')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=100, unique=True)),
                ('password', models.CharField(max_length=20)),
                ('phone', models.CharField(blank=True, default=None, max_length=9, null=True)),
                ('address', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('birthdate', models.DateField(blank=True, default=None, null=True)),
                ('image', models.ImageField(blank=True, default=None, null=True, upload_to='images/')),
                ('rooms', models.ManyToManyField(blank=True, default=None, through='app.Booking', to='app.room')),
            ],
        ),
        migrations.AddField(
            model_name='room',
            name='bookings',
            field=models.ManyToManyField(through='app.Booking', to='app.user'),
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('review', models.CharField(max_length=500)),
                ('date', models.DateTimeField()),
                ('rating', models.PositiveIntegerField(default=0, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.user')),
            ],
        ),
        migrations.AddField(
            model_name='booking',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.user'),
        ),
    ]
