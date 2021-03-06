# Generated by Django 3.1 on 2020-08-20 07:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BannedDate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Suite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=60)),
                ('image', models.ImageField(upload_to='')),
                ('description', models.TextField()),
                ('amount_per_night', models.IntegerField()),
                ('banned_dates', models.ManyToManyField(to='reservations.BannedDate')),
            ],
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('stripe_id', models.CharField(max_length=120)),
                ('status', models.CharField(max_length=15)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('suite', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='reservations.suite')),
            ],
        ),
    ]
