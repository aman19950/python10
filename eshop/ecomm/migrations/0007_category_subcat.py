# Generated by Django 2.2.3 on 2022-01-25 06:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecomm', '0006_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='subcat',
            field=models.CharField(default='jeans', max_length=50),
            preserve_default=False,
        ),
    ]