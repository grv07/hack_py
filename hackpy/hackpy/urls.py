"""hackpy URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from news.views import *

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', home),
    url(r'^home/$', home),
    url(r'^comment/(?P<news_id>\d+)/$', comment_list),
    url(r'^add/comment/$', add_comment),
    url(r'^add/reply/$', reply_form),
    url(r'^register/$', register_home),
    url(r'^add/news/$', upload_news),
    url(r'^upvote/(?P<user_id>\d+)/(?P<news_id>\d+)/$', up_vote_news),
    url(r'^crawl-now/$', scrawl_blocking_scraping),

    url(r'^login/$', login_home),
    url(r'^logout/$', logout_home),
]
