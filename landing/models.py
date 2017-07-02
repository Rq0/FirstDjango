from django.db import models


class Subscriber(models.Model):
    email = models.EmailField()
    name = models.CharField(max_length=254)

    def __str__(self):
        return "%s %s" % (self.name, self.email)

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'
