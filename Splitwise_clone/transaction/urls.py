from django.urls import  path
from . import views

urlpatterns = [
    path('transactions', views.transactions , name='transactions'),
    path('add_transaction', views.add_transaction , name='add_transaction')
    # path('add', views.add , name='add')
]
