from django.db import models

# Create your models here.
class signup(models.Model):  ## mariam
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    email = models.EmailField(max_length=254)
    status = models.CharField(max_length=50)

class Task(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=True)
    task_id=models.IntegerField(default=0)
    teacher_name = models.CharField(max_length=100)
    task_title = models.CharField(max_length=100)
    creator=models.CharField(max_length=100)
    priority = models.CharField(max_length=10, choices=(('Low', 'Low'), ('Medium', 'Medium'), ('High', 'High')))
    description = models.TextField(default="No Description!")
    completion = models.BooleanField(default=False)
