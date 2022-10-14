from django.db import models

# Create your models here.

class Todos(models.Model):
    task_name=models.CharField(max_length=200)
    user=models.CharField(max_length=150)

