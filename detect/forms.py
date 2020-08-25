from django import forms 
from .models import *
  
class HelmetForm(forms.Form): 
    helmet_Main_Img = models.ImageField(upload_to='images/') 
