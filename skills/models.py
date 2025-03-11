from django.db import models

# Create your models here.
class Skill(models.Model):
    "Generated Model"
    name = models.CharField(max_length=256,)
    
    class Meta:
        verbose_name = "Skill"
        verbose_name_plural = "Skills"

    def __str__(self):
        return self.name