from django.db import models
from django.db.models.query import QuerySet
from rest_framework import serializers
from core import models

class QuizAnsweredSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.QuizAnswered
        exclude = []

class QuizOptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.QuizOptions
        exclude = []

class QuizDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.QuizDetails
        exclude = []

class QuestionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Questions
        exclude = []