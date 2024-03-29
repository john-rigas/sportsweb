"""sportsweb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from nfl import views as nfl_views

urlpatterns = [
    path('', nfl_views.home_page, name='home'),
    #path('accounts/new', nfl_views.new_user, name = 'new_user'),
    path('accounts/login', nfl_views.login_user, name='login'),
    path('accounts/logout', nfl_views.logout_user, name='logout'),
    path('<str:user>/nfl/<int:weekno>/', nfl_views.nfl_page, name='nfl_page'),
    path('<str:user>/nfl/<int:weekno>/picks', nfl_views.picks, name='picks'),
    path('<str:user>/password/',
         nfl_views.password, name='password'),
    path('<str:user>/password/change',
         nfl_views.change_password, name='changepassword'),
    path('password', nfl_views.user_password, name='userpassword'),
    path('<str:user>/nfl/<int:weekno>/standings/', nfl_views.nfl_standings, name='nflstandings'),
    path('<str:user>/nfl/<int:weekno>/results/', nfl_views.nfl_results, name='nflresult'),
    path('<str:user>/nfl/history/', nfl_views.nfl_history, name='nflhistory'),
    path('<str:user>/nfl/history/regular/', nfl_views.nfl_history_regular, name='nflhistoryregular'),
    path('<str:user>/nfl/history/playoffs/', nfl_views.nfl_history_playoffs, name='nflhistoryplayoffs'),
    path('<str:user>/nfl/history/regular/<int:year>/', nfl_views.nfl_history_regular_year, name='nflhistoryregularyear'),
    path('<str:user>/nfl/history/playoffs/<int:year>/', nfl_views.nfl_history_playoffs_year, name='nflhistoryplayoffsyear'),
    path('<str:user>/nfl/history/<int:year>/', nfl_views.nfl_history_year, name='nflhistoryyear'),
    path('<str:user>/nfl/players/', nfl_views.nfl_players, name='nflplayers'),
    path('<str:user>/nfl/players/<str:player>/', nfl_views.nfl_player, name='nflplayer')
]
