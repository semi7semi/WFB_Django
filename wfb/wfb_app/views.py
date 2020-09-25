from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View

from wfb_app.models import Units


class Index(View):
    def get(self, request):
        units_list = Units.objects.all()
        return render(request, "index.html", {"units_list": units_list})
    def post(self, request):
        unit_id = request.POST.get('name')
        attacks = int(request.POST.get('attacks'))
        defensive = int(request.POST.get('defensive'))
        if request.POST.get('option') == "delete":
            unit = Units.objects.get(pk=unit_id)
            unit.delete()
            return redirect('/')
        if request.POST.get('option') == "fight":
            unit = Units.objects.get(pk=unit_id)
            if unit.reflex:
                ref = 1 / 6
            else:
                ref = 0
            if defensive < unit.offensive:
                result = attacks * (2/3 + ref)
                return render(request, "index.html", {"result": round(result, 2)})
            else:
                result = attacks * (1 / 2 + ref)
                return render(request, "index.html", {"result": round(result, 2)})

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
