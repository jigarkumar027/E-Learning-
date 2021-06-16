from django.db import models

# Create your models here.

class User(models.Model): #Master 
    Username = models.CharField(max_length=50,default="abc")
    Email = models.EmailField(max_length=50)
    Password = models.CharField(max_length=50)
    Role = models.CharField(max_length=50)
    OTP = models.IntegerField()
    is_created = models.DateTimeField(auto_now_add=True)
    is_update = models.DateTimeField(auto_now_add=True)
    is_verifed = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)


class Tutor(models.Model):
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    Firstname = models.CharField(max_length=50)
    Lastname = models.CharField(max_length=50)
    Address = models.CharField(max_length=50)
    Gender = models.CharField(max_length=50)
    Contact = models.CharField(max_length=50)
    Skills = models.CharField(max_length=50)
    Qaulification = models.CharField(max_length=50)
    Experience = models.CharField(max_length=50)
    DOB = models.DateField(default="2021-01-05")
    Country = models.CharField(max_length=50)
    State = models.CharField(max_length=50)
    City = models.CharField(max_length=50)
    profile_Pic = models.ImageField(upload_to="img/",default="abc.jpg")


class Student(models.Model):
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    Firstname = models.CharField(max_length=50)
    Lastname = models.CharField(max_length=50)
    Address = models.CharField(max_length=50)
    Gender = models.CharField(max_length=50)
    Contact = models.CharField(max_length=50)
    Qaulification = models.CharField(max_length=50)
    DOB = models.DateField(default="2021-02-01")
    Country = models.CharField(max_length=50)
    State = models.CharField(max_length=50)
    City = models.CharField(max_length=50)
    profile_Pic = models.ImageField(upload_to="img/",default="abc.jpg")

class Category(models.Model):
    Name = models.CharField(max_length=50)
    is_created = models.DateTimeField(auto_now_add=True)
    is_update = models.DateTimeField(auto_now_add=True)


class Course(models.Model):
    Tutor_id = models.ForeignKey(Tutor,on_delete=models.CASCADE)
    Category_id = models.ForeignKey(Category,on_delete=models.CASCADE)
    Name = models.CharField(max_length=50)
    Code = models.IntegerField()
    Description = models.CharField(max_length=100)
    Duration = models.CharField(max_length=50)
    Price = models.IntegerField()
    Technology = models.CharField(max_length=50)
    Pre_Requirment = models.CharField(max_length=50)
    course_pic = models.ImageField(upload_to="img/",default="abc.jpg")
    is_created = models.DateTimeField(auto_now_add=True)
    is_update = models.DateTimeField(auto_now_add=True) 


class Cart12(models.Model):
    Course_id = models.ForeignKey(Course,on_delete=models.CASCADE)
    Student_id = models.ForeignKey(Student,on_delete=models.CASCADE)
    total = models.IntegerField(default=0)
    subtotal = models.IntegerField(default=0)
    
    

class Transaction(models.Model):
    made_by = models.ForeignKey(User, related_name='transactions', 
                                on_delete=models.CASCADE)
    made_on = models.DateTimeField(auto_now_add=True)
    amount = models.IntegerField()
    order_id = models.CharField(unique=True, max_length=100, null=True, blank=True)
    checksum = models.CharField(max_length=100, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.order_id is None and self.made_on and self.id:
            self.order_id = self.made_on.strftime('PAY2ME%Y%m%dODR') + str(self.id)
        return super().save(*args, **kwargs)



    
