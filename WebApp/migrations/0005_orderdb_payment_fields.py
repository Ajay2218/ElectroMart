from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("WebApp", "0004_orderdb"),
    ]

    operations = [
        migrations.AddField(
            model_name="orderdb",
            name="Payment_status",
            field=models.CharField(blank=True, default="Pending", max_length=30, null=True),
        ),
        migrations.AddField(
            model_name="orderdb",
            name="Razorpay_order_id",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name="orderdb",
            name="Razorpay_payment_id",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name="orderdb",
            name="Razorpay_signature",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
