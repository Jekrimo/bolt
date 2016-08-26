from __future__ import unicode_literals
from django.db import models
from datetime import datetime
import re
import bcrypt
PASSWORD_REGEX = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[$@$!%*?&])[A-Za-z\d$@$!%*?&]{8,}')

class UserManager(models.Manager):
    def register(self,name, user_name, create_password):
        errors = []
        if user_name > 3:
            if name > 3:
                if PASSWORD_REGEX.match(create_password):
                        if not Users.objects.filter(username=user_name):
                            hashed_pass = bcrypt.hashpw(create_password.encode(), bcrypt.gensalt())
                            user = Users.objects.create(username = user_name, password = hashed_pass, name=name)
                            return (True, errors, user)
                        else:
                            errors.append('Sorry, that Username already exsists. Please Login or choose a New Username.')
                            return(False, errors)

                else:
                    if len(create_password) < 4:
                        errors.append("Password is too short!")
                    if not PASSWORD_REGEX.match(create_password):
                        errors.append("Password is invalid, please try again.")
                    if len(create_password) > 40:
                        errors.append("Password is too Long!")
                    return (False, errors)
            else:
                errors.append("Name must be at least 3 characters!")
                return (False, errors)
        else:
            errors.append("User Name must be at least 3 characters!")
            return (False, errors)

    def userlogin(self, user_name, login_password):
        from bcrypt import hashpw, gensalt
        login_errors = []
        if Users.objects.filter(username=user_name).exists() == False:
            login_errors.append("Sorry, no user found. Please try again.")
            return (False, login_errors)
        else:
            user = Users.objects.get(username=user_name)
            password = user.password.encode()
            loginpass = login_password.encode()
            if hashpw(loginpass, password) == password:
                return (True, login_errors, user)
            else:
                login_errors.append("Sorry, no password match")
                return (False, login_errors)

    def tripval(self, username, destination, description, travelfrom, travelto):
        errors = []
        if destination == "":
            errors.append("destination can not be blank!")
            return (False, errors)
        elif description == "":
            errors.append("description can not be blank!")
            return (False, errors)
        elif travelfrom < str(datetime.today()):
            errors.append("Travel From Must be a future date")
            return (False, errors)
        elif travelto < str(datetime.today()):
            errors.append("Travel to Must be a future date")
            return (False, errors)
        elif travelto < travelfrom:
            errors.append("Travel to can not be before from")
            return (False, errors)
        else:
            trip = Trip.objects.create(destination=destination, description=description, travelstart=travelfrom,travelend=travelto,createdby=username)
            return (True, errors, trip)

class Users(models.Model):
    name = models.CharField(max_length=60)
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    usermanager = UserManager()
    objects = models.Manager()


class Trip(models.Model):
    destination = models.CharField(max_length=60)
    description = models.CharField(max_length=1000)
    travelstart = models.DateTimeField()
    travelend = models.DateTimeField()
    createdby = models.CharField(max_length=60)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    users = models.ManyToManyField(Users)
    objects = models.Manager()
    tripmanager = UserManager()
