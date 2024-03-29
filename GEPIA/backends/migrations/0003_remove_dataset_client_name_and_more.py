# Generated by Django 4.2 on 2023-05-14 17:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backends', '0002_gene'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dataset',
            name='client_name',
        ),
        migrations.RemoveField(
            model_name='dataset',
            name='collection_name',
        ),
        migrations.RemoveField(
            model_name='dataset',
            name='port',
        ),
        migrations.AddField(
            model_name='dataset',
            name='has_normal',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='dataset',
            name='normal_sample_number',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='dataset',
            name='tumor_sample_number',
            field=models.IntegerField(default=0),
        ),
    ]
