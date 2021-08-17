from django.urls import path
from core.views import CreateQuiz,SubmitQuiz,GetQuiz,QuizReport,ViewQuiz,MyQuizes,QuizResult, deleteAttempted, deleteCreated

urlpatterns = [
    path('create-quiz/', CreateQuiz.as_view(),name = 'create quiz'),
    path('submit-quiz/<str:quiz_token>', SubmitQuiz.as_view(),name = 'submit quiz'),
    path('get-quiz/<str:quiz_token>', GetQuiz.as_view(),name = 'get quiz'),
    path('quiz-report/<str:quiz_token>', QuizReport.as_view(),name = 'quiz report'),
    path('view-quiz/<str:quiz_token>', ViewQuiz.as_view(),name = 'view quiz'),
    path('my-quizes/<str:username>', MyQuizes.as_view(),name = 'my quizes'),
    path('quiz-result/<str:quiz_token>', QuizResult.as_view(),name = 'quiz result'),
    path('delete-created/<str:quiz_token>', deleteCreated.as_view()),
    path('delete-attempted/<str:quiz_token>', deleteAttempted.as_view()),
]
