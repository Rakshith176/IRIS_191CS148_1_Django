from django.db import models
from isbn_field import ISBNField
from django.contrib.auth.models import User


class Book(models.Model):
      title = models.CharField(max_length = 30, unique = True, null = False)
      description = models.TextField()
      quantity = models.IntegerField()
      isbn = ISBNField(clean_isbn = False, null = False, unique = True)
      pic = models.ImageField(default = 'default.jpg', upload_to = 'book_img')

      def __str__(self):
        return self.title

      def get_photo_url(self):
        if self.pic and hasattr(self.pic, 'url'):
            return self.pic.url
        else:
            return "/media/book_img/default.jpg"

#this model extends the user model to store more info of the student
class Student(models.Model):
     user = models.OneToOneField(User,on_delete=models.CASCADE)
     roll_no = models.CharField(max_length=10, unique = True, null = False)
     is_student = models.BooleanField(default=False)

     def __str__(self):
      return self.user


issue_req=(
  ('none','NONE'),
  ('pending','PENDING'),
  ('approved','APPROVED'),
  ('rejected','REJECTED'),

)

#this model stores the transaction history
class Status(models.Model):
      stud_id = models.ForeignKey(User,on_delete = models.CASCADE)
      book_id = models.ForeignKey(Book,on_delete = models.CASCADE)
      issue_date = models.DateTimeField(null = True,blank = True)
      return_date = models.DateTimeField(null = True,blank = True)
      req = models.CharField(choices = issue_req,default = 'none',max_length = 8)


