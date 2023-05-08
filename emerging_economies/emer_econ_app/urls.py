from . import views
from django.urls import path
urlpatterns = [
    path('',views.dashboard,name="dashboard"),
    path('errorPage',views.errorPage,name="errorPage"),
    path('data',views.data,name="data"),
]
