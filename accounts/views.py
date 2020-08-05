from django.shortcuts import render, redirect
from django.contrib import messages, auth
from contacts.models import Contact
from django.contrib.auth.models import User


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You are now Logged in!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid Credentials!')
            return redirect('login')
    else:
        return render(request, 'accounts/login.html')


def register(request):
    if request.method == 'POST':
        # variables
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        # validations:-
        # password check
        if password == password2:
            # checking username
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists,Please choose some other username')
                return redirect('register')
            else:
                #checking email
                if User.objects.filter(email=email).exists():
                    messages.error(request, 'email already exists,Please use some other email')
                    return redirect('register')
                else:
                    # looks good
                    user = User.objects.create_user(username=username, email=email, first_name=first_name,
                                                    last_name=last_name, password=password)
                    user.save()
                    messages.success(request, 'you are now registered and logged in')
                    return redirect('index')
        else:
            messages.error(request, 'passwords do not match')
            return redirect('register')

    else:
        return render(request, 'accounts/register.html')


def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request,'You are logged out!')
        return redirect('index')


def dashboard(request):
    user_id = request.user.id
    inquiries = Contact.objects.order_by('-contact_date').filter(user_id=user_id)
    context = {
        'inquiries': inquiries,
    }
    return render(request, 'accounts/dashboard.html', context)
