from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator


class Treatments(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    half_hour = models.DecimalField(max_digits=6, decimal_places=2, default=55.00, validators=[MinValueValidator(1)])
    one_hour = models.DecimalField(max_digits=6, decimal_places=2, default=80.00, validators=[MinValueValidator(1)])
    two_hour = models.DecimalField(max_digits=6, decimal_places=2, default=110.00, validators=[MinValueValidator(1)])
    

    def __str__(self):
        return f"{self.title}"



class Booking(models.Model):
    BOOKING_STATUS = [
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ]
    
    treatment = models.ForeignKey(Treatments, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    duration = models.IntegerField()
    status = models.CharField(max_length=20, choices=BOOKING_STATUS, default='confirmed')
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        from datetime import datetime, timedelta
        start = datetime.combine(self.date, self.start_time)
        self.end_time = (start + timedelta(minutes=self.duration)).time()
        super().save(*args, **kwargs)

    def can_cancel(self):
        from datetime import datetime, timedelta
        booking_datetime = datetime.combine(self.date, self.start_time)
        current_datetime = datetime.now()
        time_difference = booking_datetime - current_datetime
        return time_difference.total_seconds() >= 24 * 3600

    def __str__(self):
        return f"{self.user } - {self.treatment.title} on {self.date} at {self.start_time} for {self.duration} minutes"



class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name} - {self.subject}"