from email.policy import default
from unittest.util import _MAX_LENGTH
from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
import uuid
from django.utils.translation import gettext_lazy as _
from django.conf import settings
class Users(models.Model):
    stuname=models.CharField(max_length=100)
    email = models.CharField(max_length=100)
class MyUserManager(BaseUserManager):
    def create_user(self, email, name, tc,phone, password=None, password2=None):
        """
        Creates and saves a User with the given email, name, tc and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            phone=phone,
            name=name,
            tc=tc
        )

        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self, email,phone, name,tc, password=None):
        """
        Creates and saves a superuser with the given email, name,tc and password.
        """
        user = self.create_user(
            email,
            password=password,
            phone=phone,
            name=name,
            tc=tc
        )
        user.is_admin = True
        user.save(using=self._db)
        return user
class MyUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='Email',
        max_length=255,
        unique=True,
    )
    name=models.CharField(max_length=200)
    phone=models.CharField(max_length=20,unique=True,default="")
    tc=models.BooleanField()
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    otp=models.CharField(max_length=10,default='')
    created_at=models.DateTimeField(auto_now_add=True)
    doctordiag=models.CharField(max_length=200,blank=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name','tc','phone']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

class Contact(models.Model):
    msg_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=70, default="")
    phone = models.CharField(max_length=70, default="")
    address = models.CharField(max_length=500, default="")
    city = models.CharField(max_length=50, default="")
    state = models.CharField(max_length=50, default="")
    desc = models.CharField(max_length=500, default="")


    def __str__(self):
        return self.name



class Courses(models.Model):
    course_name=models.CharField(max_length=100)

    def __str__(self):
        return self.course_name

class Questions(models.Model):
    course=models.ForeignKey(Courses, on_delete=models.CASCADE)
    questions=models.CharField(max_length=250)
    answer=models.IntegerField()
    option_one=models.CharField(max_length=100)
    option_two=models.CharField(max_length=100)
    option_three=models.CharField(max_length=100,blank=True)
    option_four=models.CharField(max_length=100,blank=True)

    def __str__(self):
        return self.Questions

class Category(models.Model):
    name=models.CharField(max_length=250)

    def __str__(self):
        return self.name
class Quizzes(models.Model):
    class Meta:
        verbose_name=_("Quiz")
        verbose_name_plural=_("Quizzes")
        ordering=['id']
    title=models.CharField(max_length=250,default=_("New Quiz"),verbose_name=_("Quiz Title"))
    category=models.ForeignKey(Category,default=1,on_delete=models.DO_NOTHING)
    date_created=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.title
class Updated(models.Model):
    date_updated=models.DateTimeField(verbose_name=_("Last Updated"),auto_now_add=True)
    class Meta:
        abstract=True
class Question(Updated):
    class Meta:
        verbose_name=_("Question")
        verbose_name_plural=_("Questions")
        ordering=['id']
    SCALE=(
        (0,_('Fundamental')),
        (1,_('Beginner')),
        (2,_('Intermediate')),
        (3,_('Advancd')),
        (4,_('Expert'))
    )
    TYPE=(
        (0,_("Multiplt Choice")),
        (1,_("MCQ"))
    )
    quiz=models.ForeignKey(Quizzes,related_name='questiom',on_delete=models.DO_NOTHING)
    technique=models.IntegerField(choices=TYPE,default=0,verbose_name=_("Type of Question"))
    title=models.CharField(max_length=250,verbose_name=_("Title"))
    difficulty=models.IntegerField(choices=SCALE,default=0,verbose_name=_("Difficulty"))
    date_created=models.DateTimeField(auto_now_add=True,verbose_name=_("Date Created"))
    is_active=models.BooleanField(default=False,verbose_name=_("Active Status"))
    def __str__(self):
        return self.title

class Answer(Updated):
    class Meta:
        verbose_name=_("Answer")
        verbose_name_plural=_("Answers")
        ordering=['id']
    question=models.ForeignKey(Question,related_name='answer',on_delete=models.DO_NOTHING)
    answer_text=models.CharField(max_length=250,verbose_name=_("Answer Text"))
    is_right=models.BooleanField(default=False)
    def __str__(self):
        return self.answer_text

class DoctorCategory(models.Model):
    name=models.CharField(max_length=250)

    def __str__(self):
        return self.name
class Doctor1(models.Model):
    msg_id = models.AutoField(primary_key=True)
    department=models.ForeignKey(DoctorCategory,on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=70, default="", null=True)
    phone = models.CharField(max_length=70, default="")
    address = models.CharField(max_length=500, default="")
    city = models.CharField(max_length=50, default="")
    state = models.CharField(max_length=50, default="")
    

    def __str__(self):
        return self.name
class Patients(models.Model):
    id=models.BigAutoField(primary_key=True)
    dtr_id=models.ForeignKey(Doctor1,default=1,on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=70, default="", null=True)
    phone = models.CharField(max_length=70, default="")
    address = models.CharField(max_length=500, default="")
    city = models.CharField(max_length=50, default="")
    state = models.CharField(max_length=50, default="")
    time=models.CharField(max_length=50, default="",blank=True)
    desc = models.CharField(max_length=1000, default="",blank=True)
    doctordiag = models.CharField(max_length=1000, default="",blank=True)
    date=models.DateField(blank=True)

    def __str__(self):
        return self.name
class PastPatient(models.Model):
    id=models.BigAutoField(primary_key=True)
    dtr_id=models.ForeignKey(Doctor1,default=1,on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=70, default="", null=True)
    phone = models.CharField(max_length=70, default="")
    address = models.CharField(max_length=500, default="")
    city = models.CharField(max_length=50, default="")
    state = models.CharField(max_length=50, default="")
    time=models.CharField(max_length=50, default="",blank=True)
    desc = models.CharField(max_length=1000, default="",blank=True)
    doctordiag = models.CharField(max_length=1000, default="",blank=True)
    date=models.DateField(blank=True)
    def __str__(self):
        return self.email