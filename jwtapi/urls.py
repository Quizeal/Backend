from django.conf.urls import url
from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from .views import RegisterApi
urlpatterns = [
      path('register/', RegisterApi.as_view()),
      path('login/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
      path('token-refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
]