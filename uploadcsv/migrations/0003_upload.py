# Generated by Django 2.0.1 on 2018-03-04 18:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('uploadcsv', '0002_auto_20180305_0243'),
    ]

    operations = [
        migrations.CreateModel(
            name='Upload',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pic', models.FileField(upload_to='images/')),
                ('upload_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
