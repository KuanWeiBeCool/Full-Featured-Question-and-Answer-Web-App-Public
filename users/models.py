from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
from PIL import Image

# Create your models here.
class Profile(models.Model):
    '''
    A class to store the information of the user. Access this class through 'user.profile'
    '''
    # This class is created because by default, Django's User class does not have a profile picture option.
    # We create this class which has a one-to-one relationship to the Django's User class as a wrapper 
    # for adding profile pictures
    user = models.OneToOneField(User, on_delete=CASCADE)
    image = models.ImageField(default='default.png', upload_to='profile_pics') # access this field through user.profile.image

    # for displaying when print out. Otherwise will just print out a Python object
    def __str__(self):
        return f"{self.user.username} Profile"

    # Update the save method to resize images
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            # max size height = width = 300
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)