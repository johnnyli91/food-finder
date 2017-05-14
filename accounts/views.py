# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect


def login_view(request):
    LOGIN_TEMPLATE = '../static/templates/login.html'

    if request.method == 'GET':
        return render(request, LOGIN_TEMPLATE)
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            error_message = {'message': 'Invalid username or password.'}
            return render(request, LOGIN_TEMPLATE, error_message)


def logout_view(request):
    logout(request)
    return redirect('index')


def sign_up(request):
    SIGN_UP_TEMPLATE = '../static/templates/sign_up.html'

    if request.method == 'GET':
        return render(request, SIGN_UP_TEMPLATE)
    elif request.method == 'POST':
        context_dict = {'message': ''}

        username = request.POST['username']
        password = request.POST['password']
        retype_password = request.POST['retype_password']

        if password != retype_password:
            context_dict['message'] = "Passwords don't match."
        elif not username:
            context_dict['message'] = "Username can't be blank."
        elif not password:
            context_dict['message'] = "Password can't be blank."
        else:
            try:
                User.objects.get(username=username)
                context_dict['message'] = "Username is already taken."
            except User.DoesNotExist:
                User.objects.create_user(username, None, password)
                user = authenticate(request, username=username, password=password)
                login(request, user)
                return redirect('index')

        return render(request, SIGN_UP_TEMPLATE, context_dict)
