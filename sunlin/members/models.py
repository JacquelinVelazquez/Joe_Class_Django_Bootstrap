from django.db import models

class Article(models.Model):
    name = models.CharField(max_length=250, default="Sin nombre", null=True, blank=True)
    content = models.TextField(default="", null=True, blank=True)

    def __str__(self):
        return self.name