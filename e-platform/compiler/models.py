from django.db import models
from ckeditor.fields import RichTextField
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.template.defaultfilters import slugify
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User

class Student(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pyscore=models.IntegerField(default=0)
    cscore=models.IntegerField(default=0)
        
    def __str__(self):
        return self.user.username


class Cquestions(models.Model):
    title=models.CharField(max_length=50)
    question=RichTextField()
    constraints=models.TextField()

    def __str__(self):
        return self.title

class Ctestcases(models.Model):
    question = models.ForeignKey(Cquestions, on_delete=models.CASCADE)
    testinput=models.TextField()
    testoutput=models.TextField()


class Ctrack(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Cquestions, on_delete=models.CASCADE)
    score = models.IntegerField()
    code = models.TextField()




class Pyquestions(models.Model):
    title=models.CharField(max_length=50)
    question=RichTextField()
    constraints=models.TextField()

    def __str__(self):
        return self.title


class Pytestcases(models.Model):
    question = models.ForeignKey(Pyquestions, on_delete=models.CASCADE)
    testinput=models.TextField()
    testoutput=models.TextField()

class Pytrack(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Pyquestions, on_delete=models.CASCADE)
    score = models.IntegerField()
    code = models.TextField()

class Ctrack(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Cquestions, on_delete=models.CASCADE)
    score = models.IntegerField()
    code = models.TextField()
