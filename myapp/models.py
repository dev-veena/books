from django.db import models

# Create your models here.
class Books(models.Model):
    book_name=models.CharField(max_length=100,unique=True)
    auther_name=models.CharField(max_length=100)
    book_price=models.PositiveIntegerField()
    total_pages=models.PositiveIntegerField()
    year=models.PositiveIntegerField(null=True)
    review=models.CharField(max_length=500,null=True,blank=True)
    image=models.ImageField(upload_to="images",null=True,blank=True)
    
    def __str__(self) :
        return self.book_name