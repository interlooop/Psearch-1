# Generated by Django 3.2.4 on 2022-02-17 09:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0017_auto_20220216_2232'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='product',
            unique_together=set(),
        ),
        migrations.RemoveField(
            model_name='product',
            name='slug',
        ),
    ]
