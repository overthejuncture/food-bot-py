from django.db import models

class Choise(models.Model):
    text = models.CharField(max_length=200)

    def __str__(self):
        return self.text
