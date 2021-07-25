from django.urls import path, include
from core.views import CreateQuiz,SubmitQuiz

urlpatterns = [
    path('create-quiz/', CreateQuiz.as_view(),name = 'create quiz'),
    path('submit-quiz/', SubmitQuiz.as_view(),name = 'submit quiz'),
]
