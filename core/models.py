from django.db import models

# Questions - id(PK), QuestionName(varchar), TypeID(FK), QuizID(FK), IsActive(bool)

# QuestionOptions - id(PK), QuestionID(FK), OptionName(varchar), IsCorrect(bool), IsActive(bool)

# QuizDetails - id(PK), QuizName(varchar), UserID(FK), StartTime(DateTime), EndTime(DateTime), IsActive(bool)

# QuizAnswered - id(PK), useID(FK), QuestionID(FK), Answer(varchar), IsActive(bool)

# QuizMarks - id(PK), QuizDetailsID(FK), userID(FK), marks(int), isActive(bool)

class Questions(models.Model):

    QUESTION_CHOICES = [
        (1, 'single_ans'),
        (2, 'multiple_ans')
    ]

    question_name = models.TextField()
    quiz_id = models.IntegerField(null = True)
    question_type = models.IntegerField(choices= QUESTION_CHOICES, default=1)
    question_marks = models.IntegerField(null = True)

class QuizDetails(models.Model):
    quiz_name = models.TextField()
    #user_id = 
    start_time = models.TimeField()
    duration = models.DurationField()
    date = models.DateField()

class QuizOptions(models.Model):
    question_id = models.IntegerField()
    option_name = models.TextField()
    is_correct = models.BooleanField()
    is_active = models.BooleanField(default=True)

class QuizAnswered(models.Model):
    #user_id = 
    question_id = models.IntegerField()
    answer = models.TextField()
    is_active = models.BooleanField(default=True)

class QuizMarks(models.Model):
    quiz_id = models.IntegerField()
    #user_id = 
    marks = models.IntegerField()
    is_active = models.BooleanField(default=True)


