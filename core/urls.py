from django.urls import path
from core.views import CreateQuiz,SubmitQuiz,GetQuiz,QuizReport,ViewQuiz,MyQuizes

urlpatterns = [
    path('create-quiz/', CreateQuiz.as_view(),name = 'create quiz'),
    path('submit-quiz/<str:quiz_token>', SubmitQuiz.as_view(),name = 'submit quiz'),
    path('get-quiz/<str:quiz_token>', GetQuiz.as_view(),name = 'get quiz'),
    path('quiz-report/<str:quiz_token>', QuizReport.as_view(),name = 'quiz report'),
    path('view-quiz/<str:quiz_token>', ViewQuiz.as_view(),name = 'view quiz'),
    path('my-quizes/<str:username>', MyQuizes.as_view(),name = 'my quizes'),
]
