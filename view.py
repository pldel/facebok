from django.shortcuts import render, redirect
from datetime import datetime
from facebook.models import User, Message, Friend

def login_view(request):
    if 'email' in request.GET and 'password' in request.GET:
        enteredEmail = request.GET['email']
        enteredPassword = request.GET['password']
        if len(User.objects.filter(email=enteredEmail).filter(password=enteredPassword))== 1:
            request.session['email'] = enteredEmail
            return redirect('/welcome')
        else:
            templates_values = {'error': 'Bad login/password/answer.'}
            return render(request, 'login.html', templates_values)
    else:
        return render(request,'login.html')


def welcome_view(request):
    if 'email' not in request.session:
        return redirect('/login')
    else:
        email = request.session['email']
        current_date_time = datetime.now()
        message = Message.objects.filter(author=User.objects.get(email=request.session['email']))
        #date = Message.publication_date(author=User.objects.get(email=request.session['email']))
        templates_values = {'datetime': current_date_time, 'email': email, 'message':message}#, 'date': date}
        return render(request, 'welcome.html', templates_values)

def registration_view(request):
    if 'email' in request.GET and 'firstname' in request.GET and 'lastname' in request.GET and 'country' in request.GET and 'phone' in request.GET and 'password' in request.GET and 'gender' in request.GET:
        if request.GET['password']==request.GET['confirm_password']:
            newUser = User(email=request.GET['email'],
            firstname=request.GET['firstname'],
            lastname=request.GET['lastname'],
            country=request.GET['country'],
            phone=request.GET['phone'],
            password=request.GET['password'],
            gender=request.GET['gender']
            )
            newUser.save()
            return redirect('/login')
        else:
            templates_values = {'error': 'Please fill in all the boxes!'}
            return render(request, 'registration.html', templates_values)
    else:
        return render(request, 'registration.html')


def add_view(request):
    if 'email' in request.session:
        if 'friend_email' in request.GET:
            if len(Friend.objects.filter(adding=request.session['email'], added=request.GET['friend_email'])) == 1:
                return render(request, 'add.html', {'error':"You're already friend with this person."})
            else:
                new_friend = Friend(adding = request.session['email'],
                added = request.GET['friend_email']
                )
                new_friend.save()
                return render(request, 'add.html', {'error':'Your friend has been successfully.'})
        else:
            return render(request, 'add.html')
    else:
        return redirect('/login')

def add_conjoint_view(request):
    if 'email' not in request.session:
        return redirect('/login')
    if 'conjoint_email' in request.GET:
        entered_email = request.GET['conjoint_email']
        if len(User.objects.filter(email=entered_email))== 1:
            logged_user = User.objects.get(email=request.session['email'])
            logged_user.conjoint = User.objects.get(email = entered_email)
            logged_user.save()
            return render(request, 'conjoint.html')
        else:
            templates_values = {'error' : 'User not found!'}
            return render(request, 'conjoint.html', templates_values)
    else:
        return render(request, 'conjoint.html')

def disconnect_view(request):
    if 'email' not in request.session:
        return redirect('/login')
    else:
        del request.session['email']
        return render(request, 'disconnect.html')

def message_view(request):
    if 'email' not in request.session:
        return redirect('/login')
    else:
        if 'text1' in request.GET:
            new_message = Message(author=User.objects.get(email=request.session['email']), content=request.GET['text1'], publication_date=datetime.now())
            new_message.save()
            return redirect('/welcome')
        else:
            return render(request, 'message.html')

def liste_amis_view(request):
    if 'email' in request.session:
        friends = Friend.objects.filter(adding=request.session['email'])
        templates_values = {'friends': friends}
        return render(request, 'listoffriends.html', templates_values)
    else:
        return redirect('/login')
