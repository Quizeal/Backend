from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from .views import LoadUserView, RegisterApi, CustomJWTSerializer

urlpatterns = [
    path("register/", RegisterApi.as_view()),
    path("load-user/", LoadUserView.as_view()),
    path(
        "login/",
        jwt_views.TokenObtainPairView.as_view(serializer_class=CustomJWTSerializer),
        name="token_obtain_pair",
    ),
    path("token-refresh/", jwt_views.TokenRefreshView.as_view(), name="token_refresh"),
]
