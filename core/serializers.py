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

    questions = serializers.PrimaryKeyRelatedField(many=True, queryset = models.Questions.objects.all())

    class Meta:
        model = models.QuizDetails
        exclude = []

class QuestionsSerializer(serializers.ModelSerializer):

    #answers = serializers.PrimaryKeyRelatedField(many=True, queryset = models.QuizAnswered.objects.all(),allow_null = True)
    options = serializers.PrimaryKeyRelatedField(many=True, queryset = models.QuizOptions.objects.all())
    class Meta:
        model = models.Questions
        exclude = []