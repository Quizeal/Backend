from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.expressions import Case
from django.db.models.fields import related

# Questions - id(PK), QuestionName(varchar), TypeID(FK), QuizID(FK), IsActive(bool)

# QuestionOptions - id(PK), QuestionID(FK), OptionName(varchar), IsCorrect(bool), IsActive(bool)

# QuizDetails - id(PK), QuizName(varchar), UserID(FK), StartTime(DateTime), EndTime(DateTime), IsActive(bool)

# QuizAnswered - id(PK), useID(FK), QuestionID(FK), Answer(varchar), IsActive(bool)

# QuizMarks - id(PK), QuizDetailsID(FK), userID(FK), marks(int), isActive(bool)

class QuizDetails(models.Model):
    quiz_name = models.TextField()
    #user_id = 
    start_time = models.TimeField()
    duration = models.DurationField()
    date = models.DateField()

class Questions(models.Model):

    QUESTION_CHOICES = [
        (1, 'single_ans'),
        (2, 'multiple_ans')
    ]

    #question_id = models.IntegerField(null = True)
    question_name = models.TextField()
    quiz_details = models.ForeignKey(QuizDetails, related_name = 'questions', on_delete=models.CASCADE,null=True)
    question_type = models.IntegerField(choices= QUESTION_CHOICES, default=1)
    question_marks = models.IntegerField(null = True)

class QuizOptions(models.Model):
    question_id = models.ForeignKey(Questions, related_name = 'options', on_delete=models.CASCADE,null=True)
    option_name = models.TextField()
    is_correct = models.BooleanField()
    is_active = models.BooleanField(default=True)

class QuizAnswered(models.Model):
    #user_id = 
    question_id = models.ForeignKey(Questions, related_name = 'answers', on_delete=models.CASCADE,null=True)
    quiz_id = models.ForeignKey(QuizDetails, on_delete=models.CASCADE,null=True)
    answer_name = models.TextField()
    is_active = models.BooleanField(default=True)

class QuizMarks(models.Model):
    quiz_id = models.ForeignKey(QuizDetails, on_delete=models.CASCADE)
    #user_id = 
    marks = models.IntegerField()
    total_marks = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self):

        return str(self.marks)


