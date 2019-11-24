from django.urls import  path
from . import views

urlpatterns = [
    path('transactions', views.transactions , name='transactions'),
    path('add_transaction', views.add_transaction , name='add_transaction'),
    path('grp_transaction', views.grp_transaction , name='grp_transaction'),
    path('add_grp_transaction', views.add_grp_transaction , name='add_grp_transaction')

]
