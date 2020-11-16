from django import forms


from .models import Armys, Units, User


class AddUnit(forms.ModelForm):
    class Meta:
        model = Units
        fields = "__all__"
        labels = {
            "name": "Nazwa",
            "offensive": "Offensive Skill",
            "strength": "Siła",
            "ap": "Armour Piercing",
            "reflex": "Czy ma Lightning Reflexes",
            "armys": "Armia"
        }
        # widgets = {
        #     "name": forms.CharField(attrs={"class":"mt-4 ml-4 mr-4"}),
        #     "offensive": forms.IntegerField(attrs={"class": "mt-4 ml-4 mr-4"}),
        #     "strength": forms.IntegerField(attrs={"class": "mt-4 ml-4 mr-4"}),
        #     "ap": forms.IntegerField(attrs={"class": "mt-4 ml-4 mr-4"}),
        #     "reflex": forms.CheckboxInput(attrs={"class": "mt-4 ml-4 mr-4"}),
        #     "army": forms.ChoiceField(attrs={"class": "mt-4 ml-4 mr-4"})
        # }

        # help_texts = {
        #     "name": "Nazwa"
        # }


class AddUser(forms.ModelForm):
    class Meta:
        model = User
        fields = "__all__"
        labels = {
            "login": "Podaj Login",
            "password": "Podaj Haslo",
            "user_armys": "Wybierz armie"
        }
        widgets = {
            "password": forms.PasswordInput()
        }