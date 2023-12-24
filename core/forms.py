
from django import forms
from .models import Post, Comment, Avatar
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserModel
from django.contrib.auth import get_user_model



class RegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class AvatarFormulario(forms.ModelForm):

    class Meta:
        model = Avatar
        fields = ["imagen"]



UserModel = get_user_model()

class EditionFormulario(UserCreationForm):
    first_name = forms.CharField(label="Nombre", widget=forms.TextInput(attrs={'placeholder': 'Ingrese su nombre'}))
    last_name = forms.CharField(label="Apellido", widget=forms.TextInput(attrs={'placeholder': 'Ingrese su apellido'}))
    email = forms.EmailField(label="Correo electrónico", widget=forms.EmailInput(attrs={'placeholder': 'Ingrese su correo electrónico'}))
    password1 = forms.CharField(label="Contraseña", widget=forms.PasswordInput(attrs={'placeholder': 'Ingrese su contraseña'}))
    password2 = forms.CharField(label="Repetir contraseña", widget=forms.PasswordInput(attrs={'placeholder': 'Repita su contraseña'}))
    
    class Meta:
        model = UserModel
        fields = ["email", "password1", "password2", "first_name", "last_name"]
        help_texts = {
            'email': 'Este campo es obligatorio.',
            'password1': 'La contraseña debe contener al menos 8 caracteres y no puede ser puramente numérica.',
            'password2': 'Repita la misma contraseña para confirmar.',
            'first_name': 'Su nombre completo, por favor.',
            'last_name': 'Su apellido completo, por favor.',
        }




class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['caption', 'image']
        labels = {
            'caption': ''
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']



class AuthenticationForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']
