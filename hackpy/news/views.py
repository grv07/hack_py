# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required

from form import *
from models import UpVoteCounter
import utils
from django.db.models import Q


#This should run async via async.io or celery
def scrawl_blocking_scraping():
    import subprocess
    r = subprocess.call("service httpd restart 1>$HOME/out 2>$HOME/error", shell=True)


def register_home(request):
    if request.method == "POST":
        user_name = request.POST.get('user_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        r_f = RegisterForm(request.POST)
        if r_f.is_valid():
            user = User.objects.filter(Q(username=user_name) | Q(email=email))
            if user:
                messages.add_message(request, messages.ERROR, 'User already exist with this email/username')
                return redirect(home)
            try:
                User.objects.create_user(username=user_name, password=password, email=email)
                user = authenticate(request, username=user_name, password=password)
                if user:
                    if user.is_active:
                        auth_login(request, user)
            except Exception as e:
                print e.args

        else:
            messages.add_message(request, messages.ERROR, 'Data not valid please try again.')

    return redirect(home)


@login_required
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
    # Show top 30 news only.
    search_on_text = request.GET.get('search_on')
    if search_on_text:
        news = News.objects.filter(story_text__search=search_on_text)
        # news = News.objects.distinct()[:30] if not news else news
        if not news:
            messages.add_message(request, messages.SUCCESS, 'news not found for this keyword.')
    else:
        news = News.objects.distinct()[:30]
    u_v_c = []
    if request.user.is_authenticated:
        u_v_c = UpVoteCounter.objects.values_list('news_id', flat=True).\
            filter(user=request.user, news__in=[n.id for n in news]).distinct()
    return render(request, 'home.html', {'newses': news, 'u_v_c': list(u_v_c)})


@login_required
def upload_news(request):
    if request.method == 'GET':
        news_form = NewsForm()
        # print news_form
        return render(request, 'news_post.html', {'form': news_form})
    else:
        news_form = NewsForm(request.POST)
        if news_form.is_valid():
            _news = news_form.save(commit=False)
            _news.hn_user = request.user.username
            _news.is_crawled = False
            _news.save()
            messages.add_message(request, messages.SUCCESS, 'news post success')
        return render(request, 'news_post.html', {'form': news_form})


@login_required
def up_vote_news(request, user_id, news_id):
    up_vote_counter = UpVoteCounter()
    up_vote_counter.user_id=user_id
    up_vote_counter.news_id=news_id
    news = News.objects.get(pk=news_id)
    if news:
        news.score += 1
        news.save()
        up_vote_counter.save()
    return redirect(home)


def comment_list(request, news_id):
    news = News.objects.prefetch_related('comment_set').filter(pk=news_id)
    comments = news[0].comment_set.all()
    sequence_comment_list = utils.reply_on_comments(comments)
    return render(request, 'comments.html', {'comments': sequence_comment_list, 'news': news[0]})


@login_required
def reply_form(request):
    if request.method == "POST":
        return render(request, 'add_review_form.html', {'comment': request.POST})
    else:
        comment_id = request.GET.get('post_in')
        if comment_id:
            comment = Comment.objects.get(pk=comment_id)
            return render(request, 'add_review_form.html', {'comment': comment})
    return redirect(home)


@login_required
def add_comment(request):
    if request.method == "POST":
        cm_form = CommentForm(request.POST)
        news_id = request.POST.get('news_id', None)
        parent_comment_id = request.POST.get('parent_comment_id', None)
        if cm_form.is_valid():
            comment = cm_form.save(commit=False)
            comment.news_id = news_id
            comment.is_crawled = False
            comment.parent_comment_id = parent_comment_id if parent_comment_id else None
            comment.save()
            messages.add_message(request, messages.INFO, 'Comment has been posted successfully.')
            return redirect(comment_list, news_id=comment.news_id)
        else:
            messages.add_message(request, messages.ERROR, 'Please try again after some time.')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        return redirect(home)


def search_text(request):
    search_on_text = request.GET.get('s_on')
    news = None
    if search_on_text:
        news = News.objects.filter(body_text__search=search_on_text)
    return redirect(home, news)

# Create your views here.

