# Generated by Django 5.2.1 on 2025-07-04 21:44

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Subscriber',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('subscribed_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('quantity', models.IntegerField(help_text='Available stock quantity', validators=[django.core.validators.MinValueValidator(0)])),
                ('coupon_code', models.CharField(blank=True, max_length=50, null=True)),
                ('discount_percentage', models.DecimalField(decimal_places=2, default=0, help_text='Discount percentage (0 to less than 100%)', max_digits=5, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(99.99)])),
                ('description', models.TextField()),
                ('color', models.CharField(max_length=50)),
                ('size', models.CharField(max_length=50)),
                ('image', models.ImageField(upload_to='product_images')),
                ('manufacturer', models.CharField(max_length=100)),
                ('rating', models.PositiveSmallIntegerField(default=0)),
                ('review_count', models.PositiveIntegerField(default=0)),
            ],
            options={
                'constraints': [models.CheckConstraint(condition=models.Q(('price__gte', 0)), name='price_non_negative'), models.CheckConstraint(condition=models.Q(('quantity__gte', 0)), name='quantity_non_negative')],
            },
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='product_varieties/')),
                ('alt_text', models.CharField(blank=True, max_length=255)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='variety_images', to='products.product')),
            ],
        ),
    ]
