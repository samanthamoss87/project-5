from django.db import models
from django.conf import settings
from django_countries.fields import CountryField

class Order(models.Model):
    PAYMENT_STATUS = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='orders'#m
    )
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    address = models.TextField()
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = CountryField()
    stripe_token = models.CharField(max_length=255)
    stripe_payment_id = models.CharField(max_length=255, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    payment_status = models.CharField(
        max_length=50, 
        choices=PAYMENT_STATUS, 
        default='pending'
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

    def __str__(self):
        status = dict(self.PAYMENT_STATUS).get(self.payment_status)
        return f"Order #{self.id} - {status} - £{self.amount}"

    def save(self, *args, **kwargs):
        """Ensure amount is always positive"""
        if isinstance(self.amount, (int, float)) and self.amount < 0:
            self.amount = abs(self.amount)
        super().save(*args, **kwargs)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"