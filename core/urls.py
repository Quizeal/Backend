from django.urls import path
from core.views import CreateQuiz,SubmitQuiz,GetQuiz,QuizReport,ViewQuiz,MyQuizes

urlpatterns = [
    path('create-quiz/', CreateQuiz.as_view(),name = 'create quiz'),
    path('submit-quiz/<int:quiz_id>', SubmitQuiz.as_view(),name = 'submit quiz'),
    path('get-quiz/<int:quiz_id>', GetQuiz.as_view(),name = 'get quiz'),
    path('quiz-report/<int:quiz_id>', QuizReport.as_view(),name = 'quiz report'),
    path('view-quiz/<int:quiz_id>', ViewQuiz.as_view(),name = 'view quiz'),
    path('my-quizes/<str:username>', MyQuizes.as_view(),name = 'my quizes'),
]
