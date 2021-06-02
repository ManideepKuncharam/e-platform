from django.conf import settings
from django.db import models
from ckeditor.fields import RichTextField
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
# Create your models here.


class Quiz(models.Model):
	user=models.ForeignKey(User,default=1,on_delete=models.CASCADE)
	name = models.CharField(max_length=100)
	description = models.CharField(max_length=70)
	quiztime=models.IntegerField(default=15)

	def __str__(self):
		return self.name


class Question(models.Model):
	quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
	question = RichTextField()


	def __str__(self):
		return self.question
	
class Answer(models.Model):
	question = models.ForeignKey(Question, on_delete=models.CASCADE)
	answer = RichTextField()
	is_correct = models.BooleanField(default=False)

	def __str__(self):
		return self.answer



class QuizTaker(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
	score = models.IntegerField(default=0)
	completed = models.BooleanField(default=False)


	def __str__(self):
		return self.user.email


class UsersAnswer(models.Model):
	quiz_taker = models.ForeignKey(QuizTaker, on_delete=models.CASCADE)
	question = models.ForeignKey(Question, on_delete=models.CASCADE)
	answer = models.ForeignKey(Answer, on_delete=models.CASCADE, null=True)

	def __str__(self):
		return self.question.label


@receiver(pre_save, sender=Quiz)
def slugify_name(sender, instance, *args, **kwargs):
	instance.slug = slugify(instance.name)