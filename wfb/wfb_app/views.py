from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.views import View

from wfb_app.forms import AddUnit, AddUser
from wfb_app.models import Units, Armys, User, GameResults, Objectives, UserArmies


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
        return render(request, "index.html")


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


class UsersView(View):
    def get(self, request):
        users_list = User.objects.all()
        user_data = []
        for user in users_list:
            userarmies = UserArmies.objects.filter(user=user.id)
            user_data += [
                {"user": user, "armies": userarmies}
            ]

        ctx = {"users_list": users_list, "user_data": user_data}
        return render(request, "users_list.html", ctx)



class AddUserView(View):
    def get(self, request):
        form = AddUser()
        ctx = {"form": form}
        return render(request, "add_user.html", ctx)
    def post(selfself, request):
        form = AddUser(request.POST)
        if form.is_valid():
            form.save()
            return redirect("main")


class EditUserView(View):
    def get(self, request, id):
        user = User.objects.get(pk=id)
        form = AddUser(instance=user)
        ctx = {"form": form}
        return render(request, "edit_user.html", ctx)

    def post(selfself, request, id):
        user = User.objects.get(pk=id)
        form = AddUser(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect("main")

class RankingView(View):
    pass



















# class Edit_unit(View):
#     def get(self, request, id):
#         unit = Units.objects.get(pk=id)
#         return render(request, "edit_unit.html", {"unit": unit})
#     def post(self, request, id):
#         unit = Units.objects.get(pk=id)
#         offensive = request.POST.get('offensive')
#         strength = request.POST.get('strength')
#         ap = request.POST.get('ap')
#         reflex_str = request.POST.get('reflex')
#         reflex = reflex_str == "on"
#         if not offensive or not strength or not ap:
#             error = "Wypelnij wszystkie pola"
#             return render(request, "edit_unit.html", {"error": error})
#         else:
#             unit.offensive = offensive
#             unit.strength = strength
#             unit.ap = ap
#             unit.reflex = reflex
#             unit.save()
#             return redirect('/')


# class Add_unit(View):
#     def get(self, request):
#         armys = Armys.objects.all()
#         return render(request, "add_unit.html", {"armys": armys})
#     def post(self, request):
#         name = request.POST.get('name')
#         offensive = request.POST.get('offensive')
#         strength = request.POST.get('strength')
#         ap = request.POST.get('ap')
#         reflex_str = request.POST.get('reflex')
#         reflex = reflex_str == "on"
#         army_id = int(request.POST.get('army'))
#         print(army_id)
#         if not name or not offensive or not strength or not ap:
#             error = "Wypelnij wszystkie pola"
#             return render(request, "add_unit.html", {"error": error})
#         else:
#             units = Units()
#             units.name = name
#             units.offensive = offensive
#             units.strength = strength
#             units.ap = ap
#             units.reflex = reflex
#             units.army = Armys.objects.get(pk=army_id)
#             units.save()
#             return redirect('/')
