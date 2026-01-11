from django.db import models

class ServiceCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class CityService(models.Model):
    category = models.ForeignKey(ServiceCategory, related_name="services", on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    contact_info = models.TextField(blank=True)

    class Meta:
        unique_together = ("category", "name")

    def __str__(self):
        return self.name
