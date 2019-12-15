from django.conf import settings
from django.db import models
from django.utils import timezone


class Sensor(models.Model):
    soil_humidity = models.DecimalField(max_digits=5, decimal_places=2)
    temperature = models.DecimalField(max_digits=5, decimal_places=2)
    humidity = models.DecimalField(max_digits=5, decimal_places=2)
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.created_date)