from django.urls import  path
from . import views

urlpatterns = [
    path('', views.index , name='index'),
    path('add_friend', views.add_friend , name='add_friend'),
    path('add_group', views.add_group , name='add_group'),
    path('add_group', views.add_group , name='add_group'),
    
    

]
