from __future__ import unicode_literals

from django.db import models

class furious(models.Model):
    name = models.CharField(max_length=100)
    content = models.TextField()
    result = models.TextField()
    def __unicode__(self):
        return self.name+self.content+self.result