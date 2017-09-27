# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout

from form import *
import utils


def register_home(request):
    if request.method == "POST":
        user_name = request.POST.get('user_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            User.objects.create_user(username=user_name, password=password, email=email)
            user = authenticate(request, username=user_name, password=password)
            if user:
                if user.is_active:
                    auth_login(request, user)
        except Exception as e:
            print e.args
            messages.add_message(request, messages.ERROR, 'Please try again after some time.')

    return redirect(home)


def logout_home(request):
    logout(request)
    return redirect(home)

def login_home(request):
    if request.method == "POST":
        username = request.POST.get('user_name')
        password = request.POST.get('password')
        if all([username, password]):
            user = authenticate(request, username=username, password=password)
            if user:
                if user.is_active:
                    auth_login(request, user)
            else:
                messages.add_message(request, messages.ERROR, 'Credentials not match')
    return redirect(home)


def home(request):
    newses = News.objects.distinct()[:30]
    return render(request, 'home.html', {'newses': newses})


def upload_news(request):
    news_form = NewsForm()
    print news_form
    return render(request, 'home.html', {'form': news_form})

def comment_list(request, news_id):
    news = News.objects.prefetch_related('comment_set').filter(pk=news_id)
    comments = news[0].comment_set.all()
    sequence_comment_list = utils.reply_on_comments(comments)
    return render(request, 'comments.html', {'comments': sequence_comment_list, 'news': news[0]})


def reply_form(request):
    if request.method == "POST":
        return render(request, 'add_review_form.html', {'comment': request.POST})
    else:
        comment_id = request.GET.get('post_in')
        if comment_id:
            comment = Comment.objects.get(pk=comment_id)
            return render(request, 'add_review_form.html', {'comment': comment})
    return redirect(home)


def add_comment(request):
    if request.method == "POST":
        cm_form = CommentForm(request.POST)
        news_id = request.POST.get('news_id', None)
        parent_comment_id = request.POST.get('parent_comment_id', None)
        print parent_comment_id
        if cm_form.is_valid():
            print cm_form
            comment = cm_form.save(commit=False)
            comment.news_id = news_id
            comment.parent_comment_id = parent_comment_id if parent_comment_id else None
            comment.save()
            messages.add_message(request, messages.INFO, 'Comment has been posted successfully.')
            return redirect(comment_list, news_id=comment.news_id)
        else:
            messages.add_message(request, messages.ERROR, 'Please try again after some time.')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        return redirect(home)
# Create your views here.
