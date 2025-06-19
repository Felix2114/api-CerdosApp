from django.db import models
from django.conf import settings
# ...code

class Cerdos(models.Model):
    url = models.URLField()
    description = models.TextField(blank=True)
    nombre = models.TextField(blank=True)
    raza = models.TextField(blank=True)
    peso = models.TextField(blank=True)
    posted_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE)


class Vote(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    cerdos = models.ForeignKey('cerdos.Cerdos', related_name='votes', on_delete=models.CASCADE)


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    cerdos = models.ForeignKey('cerdos.Cerdos', related_name='comments', on_delete=models.CASCADE)
    content = models.TextField()