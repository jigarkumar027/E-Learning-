# Generated by Django 3.2.2 on 2021-06-02 10:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='profile_Pic',
            field=models.ImageField(default='abc.jpg', upload_to='img/'),
        ),
    ]