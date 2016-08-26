from django.shortcuts import render, redirect
from . import models
from models import Users, Trip

def index(request):
    return render(request, "belt/index.html")

def createuser(request):
    if request.method == 'POST':
        if request.POST['password'] == request.POST['passconf']:
            user = Users.usermanager.register(name=request.POST['name'],user_name=request.POST['user_name'],create_password=request.POST['password'])
            if user[0] == True:
                print user[2]
                request.session['user'] = user[2].id
                return redirect('/travels')
            else:
                context = {
                    'errors' : user[1]
                }
                return render(request, "belt/index.html", context)
        else:
            context={
                'errors': 'passwords dont match'
            }
            return render(request, "belt/index.html", context)
    else:
        return redirect("/")

def login(request):
    if request.method == 'POST':
        user = Users.usermanager.userlogin(user_name=request.POST['user_name'],login_password=request.POST['logpass'])
        if user[0] == True:
            request.session['user'] = user[2].name
            print user[2].name
            return redirect('/travels')
        else:
            context = {
                'logerrors' : user[1]
            }
            return render(request, "belt/index.html", context)
    else:
        return redirect('/')
    return redirect("/")

def show(request):
    trips= Trip.objects.filter()
    name= request.session['user']
    print "(((())))"

    user= Users.objects.get(name=name)
    userid=user.id
    trips= Trip.objects.filter(createdby=name)
    tripers= Trip.objects.all()
    jointrips = Trip.objects.filter(users=user)
    print jointrips
    context={
        'usertrips' : trips,
        'joinedtrips' : jointrips,
        'tripers' : tripers,
        'user' : user
    }
    return render(request, "belt/show.html", context)

def addtrip(request):
    return render(request, "belt/add.html")

def createtrip(request):
    if request.method == 'POST':
        trip = Trip.tripmanager.tripval(username=request.session['user'], destination=request.POST['destination'],description=request.POST['description'],travelfrom=request.POST['datefrom'],travelto=request.POST['dateto'])
        if trip[0] == True:
            return redirect('/travels')
        else:
            context = {
                'triperrors' : trip[1]
            }
            return render(request, "belt/add.html", context)
    return redirect("/trip/create")

def showtrip(request, id):
    trips= Trip.objects.get(id=id)
    users = trips.users.all()
    print users
    context={
        'trip' : trips,
        'users' : trips.users.all(),
    }
    return render(request, "belt/trip.html", context)

def join(request, id):
    name=request.session['user']
    user= Users.objects.get(name=name)
    updoot= Trip.objects.get(id=id)
    updoot.users.add(user)
    return redirect('/travels')

def logout(request):
    request.session.clear()
    return redirect('/')
