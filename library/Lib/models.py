from django.db import models
from isbn_field import ISBNField
from django.contrib.auth.models import User

# Create your models here.

issue_req=(
  ('none','NONE'),
  ('pending','PENDING'),
  ('approved','APPROVED'),
  ('rejected','REJECTED'),

)


class Book(models.Model):
  Title=models.CharField(max_length=30)
  Description=models.TextField()
  Quantity=models.IntegerField()
  isbn=ISBNField(clean_isbn=False, null=False)
  pic=models.ImageField(blank=True, null=True)

  def __str__(self):
    return self.Title

class Student(models.Model):
   user=models.OneToOneField(User,on_delete=models.CASCADE)
   roll_no=models.CharField(max_length=10)
   is_student=models.BooleanField(default=False)

   def __str__(self):
    return self.user




class Status(models.Model):
  stud_id=models.ForeignKey(User,on_delete=models.CASCADE)
  book_id=models.ForeignKey(Book,on_delete=models.CASCADE)
  issue_date=models.DateTimeField(null=True,blank=True)
  return_date=models.DateTimeField(null=True,blank=True)
  req=models.CharField(choices=issue_req,default='none',max_length=8)


