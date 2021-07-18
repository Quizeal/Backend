from django.db import models

# Questions - id(PK), QuestionName(varchar), TypeID(FK), QuizID(FK), IsActive(bool)

# QuestionOptions - id(PK), QuestionID(FK), OptionName(varchar), IsCorrect(bool), IsActive(bool)

# QuestionTypes - ID(PK), TypeName(varchar)

# QuizDetails - id(PK), QuizName(varchar), UserID(FK), StartTime(DateTime), EndTime(DateTime), IsActive(bool)

# QuizAnswered - id(PK), useID(FK), QuestionID(FK), Answer(varchar), IsActive(bool)

# QuizMarks - id(PK), QuizDetailsID(FK), userID(FK), marks(int), isActive(bool)

class Questions(models.Model):

    QUESTION_CHOICES = [
        (1, 'single_ans'),
        (2, 'multiple_ans')
    ]

    question_name = models.TextField()
    type_id = models.ForeignKey("core.QuestionTypes", on_delete=models.DO_NOTHING)
    quiz_id = models.ForeignKey("core.QuizDetails", on_delete=models.CASCADE)
    question_type = models.IntegerField(choices= QUESTION_CHOICES, default=1)

class QuizOptions(models.Model):
    question_id = models.ForeignKey("core.Questions", on_delete = models.CASCADE)
    option_name = models.TextField()
    is_correct = models.BooleanField()
    is_active = models.BooleanField()

class QuizDetails(models.Model):
    quiz_name = models.CharField(max_length = 256)
    #user_id = 
    start_time = models.TimeField()
    duration = models.DurationField()
    date = models.DateField()
    quiz_marks = models.IntegerField()

class QuizAnswered(models.Model):
    #user_id = 
    question_id = models.ForeignKey("core.Questions", on_delete = models.CASCADE)
    answer = models.TextField()
    is_active = models.BooleanField()

class QuizMarks(models.Model):
    quiz_id = models.ForeignKey("core.QuizDetails", on_delete = models.CASCADE)
    #user_id = 
    marks = models.IntegerField()
    is_active = models.BooleanField()

