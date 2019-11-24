from django.shortcuts import render,redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import *
from travello.models import *

name=""
transaction_list = []
cumulative_message = ""

def cumulative(x,y):
    global cumulative_message
    myid = x
    fid = y
    obj = id_friends.objects.get(myid=myid,fid=fid)
    owe = obj.owe
    lent = obj.lent
    net = owe - lent
    if net == 0:
        cumulative_message = "All settled up!"
    elif net>0:
        cumulative_message = "You Owe " + str(net)
    else :
        cumulative_message = "You Lent " + str(-net)


# friend to friend transaction
def transactions(request):
    global transaction_list,name
    if request.method == "POST":
        fid = request.POST['fid']
        fid = int(fid)
        name = User.objects.get(id=fid).first_name
        myid = int(request.user.id)
        update_tran_list(myid,fid)
        cumulative(myid,fid)
    return render(request, 'transaction.html' , {'fid':fid ,'fname': name, 'total': cumulative_message ,'transactions': transaction_list})
# Create your views here.



 #group transactions
grp_transaction = []
details = []

other_group_detail = [] # name  total


def update_details(gid):
    global details
    user_ids_obj = group_member.objects.filter(gid=gid)
    user_ids = [x.pid for x in user_ids_obj]
    details = []
    for i in user_ids:
        obj = User.objects.get(id=i)
        details.append([obj.first_name,obj.email])

def gr_name(gid):
    return group_name.objects.get(id=gid).name

def grp_total(pid,gid):
    return group_member.objects.get(pid=pid,gid=gid).net

def other_group_detail_update(gid,pid):
    global other_group_detail
    other_group_detail = []
    other_group_detail.append(gr_name(gid))
    x = grp_total(pid,gid)
    y =""
    if x > 0:
        y = "YOU LENT Rs. "+ str(x)
    elif x <0:
        y = "YOU BORROWED Rs. " + str(-x)
    else :
        y = "All Settled Up!"
    other_group_detail.append(y)
  



def update_grp_trans_list(g_id,user_id):
    global grp_transaction
    grp_transaction = []
    gid = g_id
    transaction_id_list_obj = grp_trans_desc.objects.filter(gid=gid)
    transaction_id_list = [x.id for x in transaction_id_list_obj]
    print(user_id)
    
    for i in transaction_id_list:
        print(i)
        trans_obj_list = grp_trans.objects.filter(tid=i)
        each_trans_detail =[]
        z = grp_trans_desc.objects.get(id=i,gid=gid).desc
        each_trans_detail.append([z])
        if grp_trans.objects.filter(pid=user_id,tid=i).exists():
            obj = grp_trans.objects.get(pid=user_id,tid=i)
            s = ""
            net = obj.paid - obj.owe
            if net == 0:
                if obj.paid == 0: 
                    s = "Not Involved"
                else:
                    s = "No balance"
            elif net >0:
                s = "You Lent Rs." + str(net)
            else :
                s = "You Borrowed Rs. " + str(-net)
        else :
            s = "Not Involved"
        each_trans_detail.append([s])
        for j in trans_obj_list:
            name = User.objects.get(id=j.pid).first_name
            each_trans_detail.append([name,j.pid,j.paid,j.owe])
        
        grp_transaction.append(each_trans_detail)
    





def grp_transaction(request):
    global other_group_detail
    if request.method == "POST":
        other_group_detail = []
        myid = int(request.user.id)
        gid = int(request.POST['gid'])
        error = ""
        update_details(gid)
        update_grp_trans_list(gid,myid)
        other_group_detail_update(gid,myid)
    return render(request, 'group_transaction.html' , {'other_detail': other_group_detail,'gid':gid ,'error':error,'details': details,'grp_transaction': grp_transaction})
    



def add_grp_transaction(request):
    if request.method == 'POST':
        myid = int(request.user.id)
        gid = int(request.POST['gid'])
        desc = request.POST['description']
        money = int(request.POST['money'])
        trans_list = []

        for i,j in request.POST.items():
            if i != 'description' and i != 'money' and i != 'fid' and i[0:4] == 'paid':
                email = i[8:]
                print(email)
                pid = User.objects.get(email=email).id
                if j != "":
                    paid = int(j)
                    y = 'owed_by_' + email
                    print(y)
                    owe = int(request.POST[y])
                    print(owe)
                    trans_list.append([pid,paid,owe])
                else:
                    continue
        
        check1 = 0
        check2 = 0
        for i in trans_list:
            check1 = check1 + i[1]
            check2 = check2 + i[2]
        if money == check1 and money == check2:
            grp_trans_desc.objects.create(desc=desc,gid=gid)
            tid = grp_trans_desc.objects.latest('id').id
            print(tid)
            for i in trans_list:
                print(i)
                grp_trans.objects.create(tid=tid,gid=gid,paid=i[1],pid=i[0],owe=i[2])
                temp = group_member.objects.get(gid=gid,pid=i[0])
                x = temp.net + i[1] - i[2]
                temp.net = x
                print(x, "saldaaaaaaaaaaaaaaaaaaaaaa")
                temp.save()
            error = "successfully added"
            update_details(gid)
            print(myid)
            update_grp_trans_list(gid,myid)
            other_group_detail_update(gid,myid)
            return render(request, 'group_transaction.html' , {'other_detail': other_group_detail,'gid':gid ,'error':error,'details': details,'grp_transaction': grp_transaction})

        else:
            error = "Total money is not matching"
            update_details(gid)
            update_grp_trans_list(gid,myid)
            other_group_detail_update(gid,myid)
            return render(request, 'group_transaction.html' , {'other_detail': other_group_detail,'gid':gid ,'error':error,'details': details,'grp_transaction': grp_transaction})


#grp transaction ends
def update_tran_list(x,y):
    global transaction_list
    myid = x
    fid = y
    transaction_list =[]
    trans_list = id_trans.objects.filter(myid=myid,fid=fid)
    for i in trans_list:
            u = [i.myid,i.fid,i.desc,i.owe,i.lent , i.pbu,i.pbf,i.obu,i.obf]
            transaction_list.append(u)

def add_transaction(request):
    global transaction_list
    if request.method == "POST":
        myid = int(request.user.id)
        fid = int(request.POST['fid'])
        money = int(request.POST['money'])
        desc = request.POST['description']
        paid_by_user = int(request.POST['paid_by_user'])
        paid_by_friend = int(request.POST['paid_by_friend'])
        owed_by_user = int(request.POST['owed_by_user'])
        owed_by_friend = int(request.POST['owed_by_friend'])
        lent=0
        owe = 0
        
        name = User.objects.get(id=fid).first_name
        if money == (paid_by_friend+paid_by_user) and money == (owed_by_friend+owed_by_user):
             x1 = paid_by_user - owed_by_user
             if x1 > 0 :
                 owe = 0
                 lent = x1
             elif x1 < 0:
                 owe = -x1
                 lent = 0
             else :
                 owe =0
                 lent = 0

             id_trans.objects.create(myid=myid,fid=fid,desc=desc,owe=owe,lent=lent,pbu=paid_by_user,pbf=paid_by_friend,obu=owed_by_user,obf=owed_by_friend)
             id_trans.objects.create(myid=fid,fid=myid,desc=desc,owe=lent,lent=owe,pbu=paid_by_friend,pbf=paid_by_user,obu=owed_by_friend,obf=owed_by_user)
             print(fid,lent,owe,desc,myid)
             row1 = id_friends.objects.get(myid=myid,fid=fid)
             row2 = id_friends.objects.get(myid=fid,fid=myid)
             x = row1.lent + lent
             row1.lent = x
             y = row1.owe + owe
             row1.owe = y

             x = row2.lent + owe
             row2.lent = x
             y = row2.owe + lent
             row2.owe = y


             row1.save()
             row2.save()

             
             update_tran_list(myid,fid)
             error = 'successfully added'
             cumulative(myid,fid)
             return render(request, 'transaction.html' , {'fid':fid ,'error':error,'total': cumulative_message, 'fname': name, 'transactions': transaction_list})
        else:
            error = 'Total amount not equal to specified amount'
            update_tran_list(myid,fid)
            cumulative(myid,fid)
            return render(request, 'transaction.html' , {'fid':fid ,'error':error,'total': cumulative_message,'fname': name, 'transactions': transaction_list})

    
def settle_up(request):
    if request.method == "POST":
        myid = request.user.id
        fid = request.POST['fid']
        my = id_friends.objects.get(myid=myid,fid=fid)
        friend = id_friends.objects.get(myid=fid,fid=myid)

        x = my.owe - my.lent
        if x > 0:
            id_trans.objects.create(myid=myid,fid=fid,desc="settled up",owe=0,lent=x,pbu=x,pbf=0,obu=0,obf=x)
            id_trans.objects.create(myid=fid,fid=myid,desc="settled up",owe=x,lent=0,pbu=0,pbf=x,obu=x,obf=0)

        elif x < 0:
            id_trans.objects.create(myid=myid,fid=fid,desc="settled up",owe=-x,lent=0,pbu=0,pbf=-x,obu=-x,obf=0)
            id_trans.objects.create(myid=fid,fid=myid,desc="settled up",owe=0,lent=-x,pbu=-x,pbf=0,obu=0,obf=-x)

        my.owe = 0
        my.lent = 0
        friend.owe = 0
        friend.lent = 0
        my.save()
        friend.save()
        
        error = ''
        update_tran_list(myid,fid)
        cumulative(myid,fid)
        return render(request, 'transaction.html' , {'fid':fid ,'error':error,'total': cumulative_message,'fname': name, 'transactions': transaction_list})
