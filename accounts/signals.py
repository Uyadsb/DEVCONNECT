import os
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from profiles.models import Profile


User = get_user_model()

@receiver(post_save, sender=User)
def create_or_update_profile(sender, instance, created, **kwargs):
    # check if User created
    if created:
        Profile.objects.create(user=instance) # Création automatique du profile
    else:
        instance.profile.save()
        
        
@receiver(post_delete, sender=User)
def delete_profile(sender, instance, **kwargs):
    profile = instance.profile
    
    # delete the profile image
    if profile.avatar and profile.avatar.basename not in ['male.jpg', 'female.jbg']:
        avatar_path = profile.avatar.path
        if os.path.isfile(avatar_path):
            os.remove(avatar_path)
    # delete the profile
    profile.delete()