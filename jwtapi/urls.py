from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from .views import LoadView, RegisterApi, ChangePassword,CustomJWTSerializer

urlpatterns = [
      path('register/', RegisterApi.as_view()),
      path('load-user/', LoadView.as_view()),
      path('login/', jwt_views.TokenObtainPairView.as_view(serializer_class=CustomJWTSerializer), name='token_obtain_pair'),
      path('token-refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
      path('change-password/', ChangePassword.as_view(), name='password_change'),
]
