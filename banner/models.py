from django.db import models


class Banner(models.Model):
    image = models.ImageField(upload_to='banners')
    sequence = models.IntegerField(default=0)

    def __str__(self):
        return 'BANNER ' + str(self.sequence)
