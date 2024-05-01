from django.db import models

# Create your models here.

class Diagnostico(models.Model):
    sintomas = models.CharField(max_length=255)

    resultado = models.CharField(max_length=255)

class Symptom(models.Model):
    name = models.CharField(max_length=100)

class Disease(models.Model):
    name = models.CharField(max_length=100)
    symptoms = models.ManyToManyField(Symptom)