# in app/forms.py
from django import forms
from .models import Player
from django.contrib.auth.hashers import make_password, check_password

class RegistrationForm(forms.ModelForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput)

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
