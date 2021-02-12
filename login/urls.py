from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:pk>/results/', views.results, name='results'),
    url(r'^api/questions/$',views.vote),
    url(r'^api/send_vote/$',views.send_vote),
    url(r'^api/see_vote/$',views.see_vote),
]
