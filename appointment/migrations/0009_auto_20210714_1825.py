# Generated by Django 3.2.2 on 2021-07-14 12:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appointment', '0008_alter_profile_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='payment_completed',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AddField(
            model_name='appointment',
            name='payment_method',
            field=models.CharField(choices=[('Cash On Delivery', 'Cash On Delivery'), ('Khalti', 'Khalti'), ('Esewa', 'Esewa')], default='Cash On Delivery', max_length=20),
        ),
    ]
