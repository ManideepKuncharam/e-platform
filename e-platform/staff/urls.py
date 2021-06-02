from django.urls import path,include
from . import views

urlpatterns = [
    path('createquiz',views.createquiz,name='createquiz'),
    path("home",views.home,name="home")
]