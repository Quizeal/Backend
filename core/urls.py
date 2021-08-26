from django.urls import path
from core.views import (
    CreateQuiz,
    SubmitQuiz,
    GetQuiz,
    QuizReport,
    ViewQuiz,
    MyQuizes,
    QuizResult,
    deleteAttempted,
    deleteCreated,
)

urlpatterns = [
    path("create-quiz/<str:username>", CreateQuiz.as_view(), name="Create Quiz"),
    path(
        "submit-quiz/<str:username>/<str:quiz_token>",
        SubmitQuiz.as_view(),
        name="Submit Quiz",
    ),
    path(
        "get-quiz/<str:username>/<str:quiz_token>", GetQuiz.as_view(), name="Get Quiz"
    ),
    path(
        "quiz-report/<str:username>/<str:quiz_token>",
        QuizReport.as_view(),
        name="Quiz Report",
    ),
    path(
        "view-quiz/<str:username>/<str:quiz_token>",
        ViewQuiz.as_view(),
        name="View Quiz",
    ),
    path("my-quizes/<str:username>", MyQuizes.as_view(), name="My Quizzes"),
    path(
        "quiz-result/<str:username>/<str:quiz_token>",
        QuizResult.as_view(),
        name="Quiz Result",
    ),
    path(
        "delete-created/<str:username>/<str:quiz_token>",
        deleteCreated.as_view(),
        name="Delete Created Quiz",
    ),
    path("delete-attempted/<str:username>/<str:quiz_token>", deleteAttempted.as_view()),
]
