from django.urls import path
from core.views import CreateQuiz,SubmitQuiz,GetQuiz

urlpatterns = [
    path('create-quiz/', CreateQuiz.as_view(),name = 'create quiz'),
    path('submit-quiz/<int:quiz_id>', SubmitQuiz.as_view(),name = 'submit quiz'),
    path('get-quiz/<int:quiz_id>', GetQuiz.as_view(),name = 'get quiz'),
]
