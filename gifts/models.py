from django.db import models

class Gift(models.Model):
    STATUS_CHOICES = [
        (1, "Created"),
        (2, "Failed"),
        (3, "Processing"),
        (4, "Completed")
    ]


    phone_no = models.IntegerField()
    amount =  models.IntegerField(blank=False, null=False)
    message = models.CharField(max_length=1000)
    payment_method = models.CharField(max_length=100, null=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ipn_id = models.CharField(max_length=100, null=True)
    order_tracking_id = models.CharField(max_length=100, null=True)
    currency = models.CharField(max_length=10, null=True)

