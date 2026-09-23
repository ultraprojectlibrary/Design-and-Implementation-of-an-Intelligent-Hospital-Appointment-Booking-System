from django.db import models

class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    icon = models.ImageField(upload_to='department_icons/', null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
