from django.db import models
from skills.models import Skill
from accounts.models import User

# Create your models here.
class Profile(models.Model):
    "Generated Model"
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile",
    ) 
    bio = models.TextField(null=True, blank=True,)
    competances = models.ManyToManyField(Skill, blank=True, related_name="profile_cmpetances",)   
    
    # rigler ça 
    avatar = models.ImageField(upload_to="profile/%y/%m/%d",blank=True, null=True)  
    
    # save default image if no image is uploaded
    def save(self, *args, **kwargs):
        " check if image already exists"
        if not self.avatar:
            if self.user.sex == 'male':
                self.avatar = "profile/default/male.jpg"
            else:
                self.avatar = "profile/default/female.jpg"
        super().save(*args, **kwargs)
    
    
    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"


    def __str__(self):
        return f"{self.user.username} ({self.user.pk})"  