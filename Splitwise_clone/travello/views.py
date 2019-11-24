from django.shortcuts import render,redirect
from .models import Destination
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import *
from .forms import *
from transaction.models import *
from django.contrib.auth.base_user import AbstractBaseUser

# Create your views here.


mymessage = ""
mymessage1 = ""
friend_name_list = []
friend_id_list = []
group_list = []


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
        



def update_group_list(x):
    global group_list
    group_list =[]
    myid = x
    grp_object_list = group_member.objects.filter(pid=myid)
    grp_id_list = [i.gid for i in grp_object_list]
    for i in grp_id_list:
        y = group_name.objects.get(id=i)
        group_list.append([i, y.name])




def update_list(x):
    global friend_name_list, mymessage, friend_id_list
    # mymessage = m
    friend_name_list = []
    myid = x
    friend_list = id_friends.objects.filter(myid=myid)
    friend_id_list = []
    for i in friend_list:
        friend_id_list.append(i.fid)
    for j in friend_id_list:
        u = [str(User.objects.get(id=j).first_name), j ]
        friend_name_list.append(u)
   


def index(request):
    dest_new = Destination.objects.all()
    y = request.user.id
    if y is not None:
     update_list(int(y))
     update_group_list(int(y))
    for f in friend_name_list:
        print(f)
    return render(request,'homepage.html', {'mymessage': mymessage, 'ids': friend_id_list ,'friends': friend_name_list, 'groups' : group_list})


def add_friend(request):
    if request.method == 'POST':
        update_group_list(request.user.id)
        friend_email = request.POST['friend_email']
        if User.objects.filter(email=friend_email).exists():
            curr_user = User.objects.get(email=friend_email)
            myid = request.user.id
            fid=curr_user.id
            if id_friends.objects.filter(myid=myid,fid=fid).exists():
                update_list(int(myid))
                return render(request,'homepage.html', {'mymessage': 'already your friend', 'friends': friend_name_list, 'groups' : group_list})
            else:
                id_friends_instance = id_friends.objects.create(myid=myid,fid=fid,owe=0,lent=0)
                id_friends_instance = id_friends.objects.create(myid=fid,fid=myid,owe=0,lent=0)
                update_list(int(myid))
                return render(request,'homepage.html', {'mymessage': 'successfully added', 'friends': friend_name_list, 'groups' : group_list})
        else :
            mymessage = 'This email is not registered with splitwise'
            update_list(int(request.user.id))
            return render(request,'homepage.html', {'mymessage': mymessage, 'friends': friend_name_list, 'groups' : group_list})
    else:
        return redirect('/')


def add_group(request):
    if request.method == 'POST':
        myid = request.user.id
        update_list(int(myid))
        friend_array = []
        for i,j in request.POST.items():
            friend_array.append(j)
        grp_name = friend_array[1]

        truth = True
        for i in friend_array[2:]:
            if i != '' :
                truth = truth and User.objects.filter(email=i).exists()  
        if truth == False:
            mymessage1 = "Friend email not registered with splitwise First invite them"
            update_group_list(int(myid))
            return render(request,'homepage.html', {'mymessage1': mymessage1, 'friends': friend_name_list, 'groups' : group_list})
        else:
            group_name.objects.create(name=grp_name)
            gid = group_name.objects.latest('id').id
            for i in friend_array[2:]:
                if i!='':
                    pid = User.objects.get(email=i).id   
                    group_member.objects.create(gid=gid,pid=pid)
            
            group_member.objects.create(gid=gid,pid=myid)

            update_group_list(int(myid))
            return render(request,'homepage.html', {'mymessage1':'successfully created', 'friends': friend_name_list, 'groups' : group_list})
               
    