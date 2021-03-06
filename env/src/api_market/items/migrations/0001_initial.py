# Generated by Django 3.0.2 on 2020-04-01 20:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_title', models.CharField(max_length=100)),
                ('item_time_stamp', models.DateTimeField(auto_now_add=True)),
                ('item_condition', models.CharField(choices=[('USED', 'USED'), ('GOOD', 'GOOD'), ('NEW', 'NEW')], default='GOOD', max_length=4)),
                ('item_description', models.CharField(default='', max_length=100)),
                ('item_is_in_auction', models.BooleanField(default=False, editable=False)),
                ('item_updated', models.DateTimeField(auto_now=True)),
                ('item_image', models.ImageField(blank=True, default='no image', null=True, upload_to='', verbose_name='Uploaded image')),
                ('item_owner', models.ForeignKey(db_column='user', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'product_items',
            },
        ),
    ]
