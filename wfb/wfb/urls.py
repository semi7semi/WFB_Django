"""wfb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path

from wfb_app.views import Index, List, Calc, AddUnitView, EditUnitView, RankingView, \
    LoginView, LogoutView, UsersList, CreateUserView, EditUserView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Index.as_view(), name="main"),
    path("add_unit/", AddUnitView.as_view(), name="add-unit"),
    path('units_list/', List.as_view(), name="units-list"),

    path('edit_unit/<int:id>/', EditUnitView.as_view(), name="edit-unit"),
    path('calculator/', Calc.as_view()),

    path("ranking/", RankingView.as_view(), name="ranking"),
    path("login/", LoginView.as_view()),
    path("logout/", LogoutView.as_view(), name="logout-user"),
    path("users/", UsersList.as_view()),
    path("add_user/", CreateUserView.as_view()),
    path("edit_user/", EditUserView.as_view())

]
