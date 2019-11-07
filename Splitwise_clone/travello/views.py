from django.shortcuts import render,redirect
from .models import Destination
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import *

# Create your views here.
mymessage = ""
friend_name_list = []
def update_list(x):
    global friend_name_list, mymessage
    # mymessage = m
    friend_name_list = []
    myid = x
    friend_list = id_friends.objects.filter(myid=myid)
    friend_id_list = []
    for i in friend_list:
        friend_id_list.append(i.fid)
    for j in friend_id_list:
        friend_name_list.append(str(User.objects.get(id=j).first_name))
   


def index(request):
    dest1 = Destination()
    dest1.name = 'Mumbai'
    dest1.image = 'destination_1.jpg'
    dest1.desc = 'The city that never sleeps'
    dest1.price = 800
    dest1.offer = False

    dest2 = Destination()
    dest2.name = 'Hyderabad'
    dest2.image = 'destination_2.jpg'
    dest2.desc = 'The city that never sleeps'
    dest2.price = 1400
    dest2.offer = True


    dest3 = Destination()
    dest3.name = 'banglore'
    dest3.image = 'destination_3.jpg'
    dest3.desc = 'The city that never sleeps'
    dest3.price = 1500
    dest3.offer = False

    dest = [dest1,dest2, dest3]

    dest_new = Destination.objects.all()
    y = request.user.id
    if y is not None:
     update_list(int(y))
    for f in friend_name_list:
        print(f)
    return render(request,'homepage.html', {'mymessage': mymessage, 'friends': friend_name_list})


def add_friend(request):
    if request.method == 'POST':
        friend_name = request.POST['friend_name']
        friend_email = request.POST['friend_email']
        if User.objects.filter(email=friend_email).exists():
            curr_user = User.objects.get(email=friend_email)
            myid = request.user.id
            fid=curr_user.id
            if id_friends.objects.filter(myid=myid,fid=fid).exists():
                update_list(int(myid))
                return render(request,'homepage.html', {'mymessage': 'already your friend', 'friends': friend_name_list})
            else:
                id_friends_instance = id_friends.objects.create(myid=myid,fid=fid,owe=0,lent=0)
                id_friends_instance = id_friends.objects.create(myid=fid,fid=myid,owe=0,lent=0)
                update_list(int(myid))
                return render(request,'homepage.html', {'mymessage': 'successfully added', 'friends': friend_name_list})
        else :
            print("chaman adqkjleq11111111111111111111")
            mymessage = 'Invalid Credentials1'
            update_list(int(request.user.id))
            return render(request,'homepage.html', {'mymessage': mymessage, 'friends': friend_name_list})
    else:
        return redirect('/')