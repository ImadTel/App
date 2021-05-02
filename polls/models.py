from django.db import models

# Create your models here.


class Person(models.Model):
    firstName=models.CharField(max_length=50)
    lastName=models.CharField(max_length=60)
    birthDate=models.DateField(null=True,blank=True)

    def __str__(self):
        self.firstName + '   ' + self.lastName

    class Meta:
        verbose_name = 'Persons'
        verbose_name_plural = 'persons'


