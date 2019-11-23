from django.shortcuts import render,redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import *
from travello.models import *

transaction_list = []
def transactions(request):
    global transaction_list
    if request.method == "POST":
        fid = request.POST['fid']
        fid = int(fid)
        myid = request.user.id
        transaction_list = []
        trans_list = id_trans.objects.filter(myid=myid,fid=fid)
        for i in trans_list:
            u = [i.myid,i.fid,i.desc,i.owe,i.lent]
            transaction_list.append(u)

    return render(request, 'transaction.html' , {'fid':fid , 'transactions': transaction_list})
# Create your views here.

def add_transaction(request):
    global transaction_list
    if request.method == "POST":
        fid = int(request.POST['fid'])
        lent = int(request.POST['money'])
        owe = 0
        desc = request.POST['description']
        myid = request.user.id
        id_trans.objects.create(myid=myid,fid=fid,desc=desc,owe=0,lent=lent)
        print(fid,lent,owe,desc,myid)
        trans_list = id_trans.objects.filter(myid=myid,fid=fid)
        row = id_friends.objects.get(myid=myid,fid=fid)
        x = row.lent + lent
        row.lent = x
        row.save()
        print(row.lent)
        transaction_list = []
        for i in trans_list:
            u = [i.myid,i.fid,i.desc,i.owe,i.lent]
            transaction_list.append(u)
    return render(request, 'transaction.html' , {'fid':fid , 'transactions': transaction_list})
    
