# Generated by Django 4.1 on 2022-08-24 16:10

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Password', models.CharField(max_length=20)),
                ('Data', models.CharField(max_length=200)),
                ('image1', models.ImageField(blank=True, upload_to='images')),
            ],
        ),
    ]
