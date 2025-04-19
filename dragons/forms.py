# in app/forms.py
from django import forms
from .models import Player, Race, Dragon
from django.contrib.auth.hashers import make_password, check_password
from datetime import date
from django.forms.widgets import RadioSelect

class RegistrationForm(forms.ModelForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput)
    starter_race = forms.ModelChoiceField(
        queryset=Race.objects.all(),
        widget=RadioSelect,           # <-- render as radio inputs
        empty_label=None,
        label="Choose your dragon’s race"
    )

    starter_sex = forms.ChoiceField(
        choices=[('Male','Male'),('Female','Female')],
        widget=RadioSelect,           # <-- render as radio inputs
        label="Choose your dragon’s sex"
    )
    class Meta:
        model = Player
        fields = ['name', 'mail']

    def clean_password2(self):
        p1 = self.cleaned_data.get('password1')
        p2 = self.cleaned_data.get('password2')
        if p1 != p2:
            raise forms.ValidationError("Passwords do not match")
        return p2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.pwd = make_password(self.cleaned_data['password1'])
        if commit:
            user.save()


            # now create their starter dragon
            race = self.cleaned_data['starter_race']
            sex  = self.cleaned_data['starter_sex']
            Dragon.objects.create(
                name      = f"{user.name}'s {race.name}",
                race      = race,
                specie    = "dragon",
                height    = 10,
                sex       = sex,
                age       = "a few hours",
                weight    = 5.0,
                born_on   = date.today(),
                owner     = user,
				GP        = 350,
				BLUP      = -100,
				bred_by   = user,
            )

        return user

class LoginForm(forms.Form):
    mail     = forms.EmailField(label="Email")
    password = forms.CharField(widget=forms.PasswordInput, label="Password")

    def clean(self):
        data = super().clean()
        try:
            user = Player.objects.get(mail=data.get('mail'))
        except Player.DoesNotExist:
            raise forms.ValidationError("No user with that email")
        if not check_password(data.get('password'), user.pwd):
            raise forms.ValidationError("Wrong password")
        data['user'] = user
        return data
