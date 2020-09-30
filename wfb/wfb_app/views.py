from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View

from wfb_app.models import Units


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
        units_list = Units.objects.all()
        return render(request, "index.html", {"units_list": units_list})
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
            return redirect(f'edit_unit/{unit.id}/')
        if request.POST.get('option') == "fight":
            unit = Units.objects.get(pk=unit_id)
            if unit.reflex:
                ref = 1 / 6
            else:
                ref = 0
            if defensive < unit.offensive:
                hit = attacks * (2/3 + ref)
                wounds = towound(hit, unit.strength, resistance)
                arm = []
                for armour in range(1, 7):
                    wounds_after_armour = afterarmour(unit.ap, armour, wounds)
                    arm.append(wounds_after_armour)
                return render(request, "index.html", {"hit": round(hit, 2), "wounds": round(wounds, 2), "arm": arm})
            else:
                hit = attacks * (1 / 2 + ref)
                wounds = towound(hit, unit.strength, resistance)
                arm = []
                for armour in range(1, 7):
                    wounds_after_armour = afterarmour(unit.ap, armour, wounds)
                    arm.append(wounds_after_armour)
                return render(request, "index.html", {"hit": round(hit, 2), "wounds": round(wounds, 2), "arm": arm})



class Edit_unit(View):
    def get(self, request, id):
        unit = Units.objects.get(pk=id)
        return render(request, "edit_unit.html", {"unit": unit})
    def post(self, request, id):
        unit = Units.objects.get(pk=id)
        offensive = request.POST.get('offensive')
        strength = request.POST.get('strength')
        ap = request.POST.get('ap')
        reflex_str = request.POST.get('reflex')
        reflex = reflex_str == "on"
        if not offensive or not strength or not ap:
            error = "Wypelnij wszystkie pola"
            return render(request, "edit_unit.html", {"error": error})
        else:
            unit.offensive = offensive
            unit.strength = strength
            unit.ap = ap
            unit.reflex = reflex
            unit.save()
            return redirect('/')



class Add_unit(View):
    def get(self, request):
        return render(request, "add_unit.html")
    def post(self, request):
        name = request.POST.get('name')
        offensive = request.POST.get('offensive')
        strength = request.POST.get('strength')
        ap = request.POST.get('ap')
        reflex_str = request.POST.get('reflex')
        reflex = reflex_str == "on"
        if not name or not offensive or not strength or not ap:
            error = "Wypelnij wszystkie pola"
            return render(request, "add_unit.html", {"error": error})
        else:
            units = Units()
            units.name = name
            units.offensive = offensive
            units.strength = strength
            units.ap = ap
            units.reflex = reflex
            units.save()
            return redirect('/')

class List(View):
    def get(self, request):
        units_list = Units.objects.all()
        return render(request, "units_list.html", {"units_list": units_list})
