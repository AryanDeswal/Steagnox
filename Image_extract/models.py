from django.db import models

class Ext_Image(models.Model):
    Password = models.CharField(max_length=20,)
    image2 = models.ImageField(upload_to='images', blank=True)

    def __str__(self):
        return self.title
