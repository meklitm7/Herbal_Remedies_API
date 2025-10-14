from django.db import models
from django.contrib.auth.models import User


# Create your models here.
 

class Herb(models.Model):
    CATEGORY_CHOICES = [
        ('leaf', 'Leaf'),
        ('root', 'Root'),
        ('seed', 'Seed'),
        ('flower', 'Flower'),
        ('bark', 'Bark'),
        ('fruit', 'Fruit'),
        ('stem', 'Stem'),
        ('other', 'Other'),

    ]
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    other_category_explanation = models.TextField(blank=True, null=True)
    description = models.TextField()
    uses = models.TextField()
    ailments = models.TextField(
        blank=True,null=True,help_text="Comma-separated list of ailments this herb treats, e.g., 'headache, fever'")
    precautions = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='herb_images/', blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='herbs')
    class Meta:
        unique_together = ('name', 'uses', 'created_by') 

    def __str__(self):
        return self.name
class Collection(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="collections")
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    herbs = models.ManyToManyField('Herb', related_name='collections', blank=True)

    def __str__(self):
        return self.name


