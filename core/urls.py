from django.urls import path, include
from core.views import CreateQuiz,SubmitQuiz,GetQuiz

urlpatterns = [
    path('create-quiz/', CreateQuiz.as_view(),name = 'create quiz'),
    path('submit-quiz/', SubmitQuiz.as_view(),name = 'submit quiz'),
    path('get-quiz/', GetQuiz.as_view(),name = 'get quiz'),
]
