from django.db import models
from tinymce.models import HTMLField

from users.models import User

class ArticleCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class ArticleTag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Article(models.Model):
    title = models.CharField(max_length=200)
    category = models.ForeignKey(ArticleCategory, on_delete=models.SET_NULL, null=True)
    tags = models.ManyToManyField(ArticleTag, blank=True)
    content = HTMLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.title}-{self.category.name}'

    def get_absolute_url(self):
        return f'/wiki/{self.id}'

class ArticleHistory(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='history')
    title = models.CharField(max_length=200)
    content = models.TextField()
    edited_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    comment = models.CharField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.article.title}-{self.created_at}'

class ConfigTemplate(models.Model):
    name = models.CharField(max_length=200)
    device_type = models.ForeignKey('devices.DeviceType', on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    config_text = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name}'

