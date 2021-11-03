from django.urls import path

from users.views import UserDetailView, UserUpdateView, UserRegistrationView, UserPasswordChangeView, UserLoginView


urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('register/', UserRegistrationView.as_view(), name='registration'),
    path('change_password/', UserPasswordChangeView.as_view(), name='change_password'),
    path('<int:pk>/', UserDetailView.as_view(), name='user_detail'),
    path('<int:pk>/update/', UserUpdateView.as_view(), name='user_update'),

]
