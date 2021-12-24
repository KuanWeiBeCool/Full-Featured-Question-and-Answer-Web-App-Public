from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver

from .models import Profile

# when a user is saved, send the signal to the create_profile function. 
# The create_profile function is the receiver, and takes the arguments
# that post_save passes to it
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    # if the user is created, let create a Profile object with the user equals to the instance of the user that was created
    if created:
        Profile.objects.create(user=instance)

    
@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    # save the profile when the user is saved
    instance.profile.save()