from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^main/(?P<num>\d+)$', views.user_page),
    url(r'^addbook$', views.addbook),
    url(r'^book/(?P<num>\d+)$', views.book_page),
    url(r'^addfavorite/(?P<num>\d+)$', views.add_favorite),
    url(r'^unfavorite/(?P<num>\d+)$', views.unfavorite),
    url(r'^remove/(?P<num>\d+)$', views.remove),
]
