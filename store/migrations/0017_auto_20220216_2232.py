# Generated by Django 3.2.4 on 2022-02-16 21:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0016_alter_product_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='dateDelivered',
        ),
        migrations.RemoveField(
            model_name='order',
            name='datePaid',
        ),
        migrations.RemoveField(
            model_name='order',
            name='isDelivered',
        ),
        migrations.RemoveField(
            model_name='order',
            name='isPaid',
        ),
        migrations.RemoveField(
            model_name='order',
            name='shippingPrice',
        ),
        migrations.RemoveField(
            model_name='order',
            name='taxPrice',
        ),
        migrations.RemoveField(
            model_name='order',
            name='totalPrice',
        ),
    ]
