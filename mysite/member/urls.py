from django.urls import path
from . import views
from .views import CustomLoginView, RegisterPage, TripList
from django.contrib.auth.views import LogoutView

app_name = 'member'

urlpatterns = [
    path("", TripList.as_view(), name="triplist"),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/',LogoutView.as_view(next_page='member:login'), name="logout"),
    path('register/',RegisterPage.as_view(), name='register'),
]
