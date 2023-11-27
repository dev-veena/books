# Generated by Django 4.2.6 on 2023-10-31 05:11

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Books',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('book_name', models.CharField(max_length=100)),
                ('auther_name', models.CharField(max_length=100)),
                ('book_price', models.PositiveIntegerField()),
                ('total_pages', models.PositiveIntegerField()),
            ],
        ),
    ]