# Generated by Django 3.2.4 on 2021-07-04 17:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0002_auto_20210628_2043'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profession',
            field=models.CharField(blank=True, choices=[('Developer', 'developer'), ('Software Engineer', 'Software engineer'), ('Data Analyst', 'Data Analyst')], max_length=40, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='profile_picture',
            field=models.ImageField(default='/media/default.jpg', upload_to='media/profile_pics'),
        ),
    ]
