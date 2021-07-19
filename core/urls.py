from django.urls import path, include
from core.views import CreateQuiz

urlpatterns = [
    path('', CreateQuiz.as_view(),name = 'create quiz')
]
