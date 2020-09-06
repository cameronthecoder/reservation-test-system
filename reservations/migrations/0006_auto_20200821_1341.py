# Generated by Django 3.1 on 2020-08-21 18:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0005_auto_20200820_2020'),
    ]

    operations = [
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=60)),
                ('image', models.ImageField(upload_to='')),
                ('active', models.BooleanField(default=True)),
                ('description', models.TextField()),
                ('amount_per_night', models.IntegerField(help_text='Amount in USD')),
                ('banned_dates', models.ManyToManyField(blank=True, help_text='You may ban certain dates from being reserved for this room by adding them to this list.', to='reservations.BannedDate')),
            ],
        ),
        migrations.RemoveField(
            model_name='reservation',
            name='suite',
        ),
        migrations.DeleteModel(
            name='Suite',
        ),
        migrations.AddField(
            model_name='reservation',
            name='room',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='reservations.room'),
        ),
    ]