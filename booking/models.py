from django.db import models


class Treatments(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    half_hour = models.DecimalField(max_digits=6, decimal_places=2, default=55.00)
    one_hour = models.DecimalField(max_digits=6, decimal_places=2, default=80.00)
    two_hour = models.DecimalField(max_digits=6, decimal_places=2, default=110.00)
    

    def __str__(self):
        return f"{self.title}"



class Booking(models.Model):
    treatment = models.ForeignKey(Treatments, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    duration = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        from datetime import datetime, timedelta
        start = datetime.combine(self.date, self.start_time)
        self.end_time = (start + timedelta(minutes=self.duration)).time()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.treatment.title} on {self.date} at {self.start_time} for {self.duration} minutes"



class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name} - {self.subject}"