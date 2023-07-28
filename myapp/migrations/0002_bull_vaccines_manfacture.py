# Generated by Django 4.1.7 on 2023-04-23 15:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bull',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bull_id', models.CharField(max_length=28)),
                ('bull_name', models.CharField(max_length=28)),
                ('breed', models.CharField(blank=True, max_length=28)),
            ],
        ),
        migrations.AddField(
            model_name='vaccines',
            name='manfacture',
            field=models.CharField(blank=True, max_length=28),
        ),
    ]
