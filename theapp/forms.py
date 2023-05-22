from django import forms
from .models import Location, Event, Ticket
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages

class SignupForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de usuario'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirmar contraseña'}))
    email = forms.EmailField(label='Correo electrónico')

    class Meta:
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control'})
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
    
        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', 'Las contraseñas no coinciden.')



class loginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de usuario'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'}))

class createNewLocation(forms.ModelForm):
    class Meta:
        model = Location
        fields = {'name', 'max_tickets'}
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'max_tickets': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class createNewEvent(forms.ModelForm):
    class Meta:
        model = Event
        fields = {'name', 'date', 'idLocation'}
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control'}),
            'idLocation': forms.Select(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super(createNewEvent, self).__init__(*args, **kwargs)
        self.fields['idLocation'].queryset = Location.objects.all()

class createNewTicket(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = {'nameUser','email','numTickets','idEvent'}
        widgets = {
            'nameUser': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'numTickets': forms.NumberInput(attrs={'class': 'form-control'}),
            'idEvent': forms.HiddenInput(),   
        } 