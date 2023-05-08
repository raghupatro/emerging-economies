from . import views
from django.urls import path
urlpatterns = [
    path("", views.index, name="index"),
    path('home',views.home,name="home"),
    path('errorPage',views.errorPage,name="error"),
    path('dashboard',views.dashboard,name="dashboard"),
]
