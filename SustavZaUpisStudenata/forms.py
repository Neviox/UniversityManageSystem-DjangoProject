import email
from tkinter import Widget
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import Korisnici, Predmeti

User = get_user_model()

##LOGIN FORM
class LoginForm(forms.Form):
    Email    = forms.EmailField(label='Email')
    Password = forms.CharField(widget=forms.PasswordInput)


##REGISTER FORM
class RegisterForm(forms.ModelForm):
    
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('Email','Status','Roles')

    def check_password(self):
        
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        
        user = super(RegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        
        if commit:
            user.save()
        return user



##CREATE SUBJECT
class SubjectCreate(forms.ModelForm):
    
    
    NositeljKolegija = forms.ModelChoiceField(queryset=Korisnici.objects.filter(Roles_id=2))
    
    class Meta:
        model = Predmeti
        exclude = ('Upisni',)
        fields = '__all__'
        
  
        

##CREATE STUDENT
class StudentCreate(forms.ModelForm):
    class Meta:
        model = Korisnici
        exclude = ('last_login',)
        fields = '__all__'

##SUBJECT LIST
class SubjectView(forms.ModelForm):
    Ime = forms.CharField(
        widget=forms.TextInput(attrs={'readonly':'readonly'})
    )
    Kod = forms.CharField(
        widget=forms.TextInput(attrs={'readonly':'readonly'})
    )
    Program = forms.CharField(
        widget=forms.TextInput(attrs={'readonly':'readonly'})
    )
    Bodovi = forms.IntegerField(
        widget=forms.TextInput(attrs={'readonly':'readonly'})
    )
    Sem_redovni = forms.IntegerField(
        widget=forms.TextInput(attrs={'readonly':'readonly'})
    )
    Izborni = forms.CharField(
        widget=forms.TextInput(attrs={'readonly':'readonly'})
    )
    

    class Meta:
        model = Predmeti
        fields = '__all__'
