from django.db import models

class Booking(models.Model):
    first_name = models.CharField(max_length=200)
    reservation_date = models.DateField()
    reservation_slot = models.SmallIntegerField(default=10)

    def __str__(self): 
        return self.first_name

class Menu(models.Model):
   title = models.CharField(max_length=200) 
   price = models.IntegerField(null=False, blank = False) 
   inventory = models.IntegerField(null = False, blank = False)

   def __str__(self):
      return self.title