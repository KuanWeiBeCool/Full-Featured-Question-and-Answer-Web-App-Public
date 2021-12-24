from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django_quill.fields import QuillField

# Create your models here.
class Post(models.Model):
    # title field that has a max length of 100 characters
    title = models.CharField(max_length=100)
    # content = models.TextField()
    content = QuillField(null=True)
    date_posted = models.DateTimeField(default=timezone.now)
    category = models.CharField(max_length=100, default="General")
    # as each user can have multiple posts, post and user have an one-to-many relationships. 
    # So we need to set the author to be the foreign key. 
    # When a user is deleted, we need to delete their all posts. So on_delete is set to CASCADE
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, related_name='blog_post')
    
    # This function calculates the total likes of a post
    def total_likes(self):
        return self.likes.count()
    
    
    
    # This function sets how the post objects are displayed when being called.
    def __str__(self) -> str:
        return self.title
    
    # This function helps get the exact url as a string for redirect
    def get_absolute_url(self):
        return reverse("post-detail", kwargs={"pk": self.pk})
    
    
class Category(models.Model):
    name = models.CharField(max_length=100, default="General")
    # This function sets how the post objects are displayed when being called.
    def __str__(self) -> str:
        return self.name
    
    # This function helps get the exact url as a string for redirect
    def get_absolute_url(self):
        return reverse('home')
    
    
class Comment(models.Model):
    # as each post can have multiple comments, comment and post have an one-to-many relationships. 
    # So we need to set the author to be the foreign key. 
    # When a post is deleted, we need to delete their all comments. So on_delete is set to CASCADE
    post = models.ForeignKey(Post, related_name="comment", on_delete=models.CASCADE)
    # content = models.TextField()
    content = QuillField(null=True)
    date_posted = models.DateTimeField(default=timezone.now)

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, related_name='blog_comment')
    
        # This function sets how the post objects are displayed when being called.
    def __str__(self) -> str:
        return self.post.title
    
    # This function helps get the exact url as a string for redirect
    def get_absolute_url(self):
        return reverse("post-detail", kwargs={"pk": self.post.pk})