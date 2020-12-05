from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.views import View
from django.views.generic import FormView, ListView

from wfb_app.forms import AddUnit, LogForm, RegisterUserForm, ProfileForm, EditUserForm, GameResultsForm
from wfb_app.models import Units, Armys, GameResults, Objectives, Profile
from django.contrib.auth.models import User


def towound(hit, st, res):
    if st - res >= 2:
        wounds = hit * 5 / 6
    elif 2 > st - res >= 1:
        wounds = hit * 2 / 3
    elif 1 > st - res >= 0:
        wounds = hit / 2
    elif 0 > st - res >= -1:
        wounds = hit / 3
    else:
        wounds = hit / 6
    return round(wounds, 1)

def afterarmour(ap, arm, wounds):
    if arm - ap <= 0:
        wounds_armour = wounds
    elif 0 < arm - ap <= 1:
        wounds_armour = wounds * 5 / 6
    elif 1 < arm - ap <= 2:
        wounds_armour = wounds * 2 / 3
    elif 2 < arm - ap <= 3:
        wounds_armour = wounds / 2
    elif 3 < arm - ap <= 4:
        wounds_armour = wounds / 3
    else:
        wounds_armour = wounds / 6
    return round(wounds_armour, 1)

class Index(View):
    def get(self, request):
        users = User.objects.all()
        no_of_games = GameResults.objects.all().count()

        ctx = {"no_of_users": users.count(), "no_of_games": no_of_games}
        return render(request, "index.html", ctx)


class Calc(View):
    def get(self, request):
        units_list = Units.objects.all()
        return render(request, "calculator.html", {"units_list": units_list})
    def post(self, request):
        unit_id = request.POST.get('name')
        attacks = int(request.POST.get('attacks'))
        defensive = int(request.POST.get('defensive'))
        resistance = int(request.POST.get('resistance'))
        if request.POST.get('option') == "delete":
            unit = Units.objects.get(pk=unit_id)
            unit.delete()
            return redirect('/')
        if request.POST.get('option') == "edit":
            unit = Units.objects.get(pk=unit_id)
            return redirect(f'/edit_unit/{unit.id}/')
        if request.POST.get('option') == "fight":
            unit = Units.objects.get(pk=unit_id)
            if unit.reflex:
                ref = 1 / 6
            else:
                ref = 0
            if defensive < unit.offensive:
                hit = attacks * (2 / 3 + ref)
                wounds = towound(hit, unit.strength, resistance)
                saves = ["0", "6+", "5+", "4+", "3+", "2+", "1+"]
                arm = []
                for armour in range(0, 7):
                    wounds_after_armour = afterarmour(unit.ap, armour, wounds)
                    arm.append(wounds_after_armour)
                return render(request, "calculator.html",
                              {"hit": round(hit, 2), "wounds": round(wounds, 2), "arm": arm, "saves": saves,
                               "unit": unit})
            else:
                hit = attacks * (1 / 2 + ref)
                wounds = towound(hit, unit.strength, resistance)
                saves = ["none", "6+", "5+", "4+", "3+", "2+", "1+"]
                arm = []
                for armour in range(0, 7):
                    wounds_after_armour = afterarmour(unit.ap, armour, wounds)
                    arm.append(wounds_after_armour)
                return render(request, "calculator.html",
                              {"hit": round(hit, 2), "wounds": round(wounds, 2), "arm": arm, "saves": saves,
                               "unit": unit})


class List(View):
    def get(self, request):
        units_list = Units.objects.all().order_by("name")
        return render(request, "units_list.html", {"units_list": units_list})


class AddUnitView(View):
    def get(self, request):
        form = AddUnit()
        ctx = {"form": form}
        return render(request, "add_unit.html", ctx)
    def post(self, request):
        form = AddUnit(request.POST)
        if form.is_valid():
            form.save()
            return redirect("units-list")


class EditUnitView(View):
    def get(self, request, id):
        unit = Units.objects.get(pk=id)
        form = AddUnit(instance=unit)
        ctx = {"form": form}
        return render(request, "edit_unit.html", ctx)
    def post(self, request, id):
        unit = get_object_or_404(Units, pk=id)
        form = AddUnit(request.POST, instance=unit)
        if form.is_valid():
            form.save()
            return redirect("units-list")


class LoginView(FormView):
    form_class = LogForm
    template_name = "login_form.html"
    success_url = "/"

    def form_valid(self, form):
        username = form.cleaned_data["login"]
        password = form.cleaned_data["password"]
        user = authenticate(self.request, username=username, password=password)
        if user:
            login(self.request, user)
            return super().form_valid(form)
        form.add_error(None, "Zły login lub haslo")
        return super().form_invalid(form)


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("/")


class CreateUserView(View):
    def get(self, request):
        form = RegisterUserForm()
        profile_form = ProfileForm()
        ctx = {"form": form, "profile_form": profile_form}
        return render(request, "user_form.html", ctx)
    def post(self, request):
        form = RegisterUserForm(request.POST)
        profile_form = ProfileForm(request.POST)
        if form.is_valid() and profile_form.is_valid():
            user = form.save()
            user.set_password(form.cleaned_data["password"])
            user.save()
            user_army = profile_form.cleaned_data["user_army"]
            Profile.objects.create(
                user_army = user_army,
                user = user
            )
            return redirect("users-list")
        else:
            ctx = {"form": form, "profile_form": profile_form}
            return render(request, "user_form.html", ctx)


class EditUserView(View):
    def get(selfself, request, id):
        user = User.objects.get(pk=id)
        form = EditUserForm(instance=user)
        profile_form = ProfileForm(instance=user.profile)
        return render(request, "user_form.html", {
            "form": form,
            "profile_form": profile_form
        })
    def post(self, request, id):
        user = User.objects.get(pk=id)
        form = EditUserForm(request.POST, instance=user)
        profile_form = ProfileForm(request.POST, instance=user.profile)
        if form.is_valid() and profile_form.is_valid():
            form.save()
            profile_form.save()
            return redirect("users-list")


class UsersList(ListView):
    model = User
    context_object_name = "users"


class DeleteUser(View):
    def get(self, request, id):
        user = User.objects.get(pk=id)
        user.delete()
        return redirect("users-list")


class RankingList(View):
    def get(self, request):
        ranking = GameResults.objects.all()
        return render(request, "ranking_list.html", {"ranking": ranking})
    def post(self, request):
        if request.POST.get("option") == "name_sort":
            ranking = GameResults.objects.all().order_by("user", "-battle_points")
            return render(request, "ranking_list.html", {"ranking": ranking})
        if request.POST.get("option") == "points_sort":
            ranking = GameResults.objects.all().order_by("-battle_points")
            return render(request, "ranking_list.html", {"ranking": ranking})
        if request.POST.get("option") == "rank_sort":
            ranking = GameResults.objects.all().order_by("-game_rank")
            return render(request, "ranking_list.html", {"ranking": ranking})
        else:
            ranking = GameResults.objects.all()
            return render(request, "ranking_list.html", {"ranking": ranking})



class AddGameResultView(View):
    def get(self, request):
        form = GameResultsForm()
        ctx = {"form": form}
        return render(request, "ranking_form.html", ctx)
    def post(self, request):
        form = GameResultsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("ranking-list")
        else:
            ctx = {"form": form}
            return render(request, "ranking_form.html", ctx)
