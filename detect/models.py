from django.db import models

# Create your models here.
class Helmet(models.Model): 
    helmet_Main_Img = models.ImageField(upload_to='images/') 

    class Meta:
        db_table='helmet'