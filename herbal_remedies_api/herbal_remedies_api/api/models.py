from django.db import models
from django.contrib.auth.models import User


# Create your models here.
 

class Herb(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    description = models.TextField()
    uses = models.TextField()
    precautions = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='herbs')
    class Meta:
        unique_together = ('name', 'uses', 'created_by') 

    def __str__(self):
        return self.name

