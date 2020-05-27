from django.db import models
from accounts.models import User
# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255, help_text='category description')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['-created_at']


class Blog(models.Model):
    title = models.CharField(max_length=500)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, auto_created='blog_category')
    content = models.TextField()
    published = models.BooleanField(default=False)
    by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


# class BlogInteraction(models.Model) :
#     blogId = models.ForeignKey(Blog , on_delete = models.CASCADE , related_name = 'blogInteraction')
#     by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blogInteraction')
#     comment = models.CharField(max_length=500)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     interactionType =  models.CharField(max_length=100)