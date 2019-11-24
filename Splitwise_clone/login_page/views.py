from django.shortcuts import render,redirect
from django.contrib.auth.models import User, auth
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
# Create your views here.

error  = ""
def change(request):
    global error
    if request.method == 'POST':
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        password = request.POST['password']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        z= request.user.id
        y = User.objects.get(id=z)
        if User.check_password(y,password):
            if password1 == password2:
                y.set_password(password1)
                if firstname != "":
                    y.first_name = firstname
                if lastname != "":
                    y.last_name = lastname
                y.save()
                return redirect("/")
            else:
                error = "new password didn't match"
        else:
            error = "Old password was incorrect"
        
    error = ""
    return render(request, 'change_pass.html', {'error': error })



def register(request):   
    if request.method == 'POST' :
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                print('already taken')
                messages.info(request,'Username Taken')
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                print('email taken')
                messages.info(request, 'Email Taken')
                return  redirect('register')
            else:
                user = User.objects.create_user(username=username,email=email,password = password1,first_name= first_name,last_name = last_name)
                user.save();
                print('user created')
                return redirect('login')
        else :
            # print('password not matched')
            messages.info(request,'Password not matched')
            return redirect('register')
    else :
        return render(request, 'register_new.html', {'data': 'null'})


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username= username, password = password)
        if user is not None:
            auth.login(request,user)
            return redirect('/')
        else:
            messages.info(request,'Invalid Credentials')
            return redirect('login')

    
    else:
        return render(request, 'login_new.html')


def logout(request):
    auth.logout(request)
    return redirect('/')