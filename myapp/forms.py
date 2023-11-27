from django import forms
from myapp.models import Books
from django.contrib.auth.models import User

class BooksModelForm(forms.ModelForm):
    class Meta:
        model=Books
        fields="__all__"

        widgets={ 
            'book_name':forms.TextInput(attrs={'class':'form-control'}),
            'auther_name':forms.TextInput(attrs={'class':'form-control'}),
            'book_price':forms.NumberInput(attrs={'class':'form-control'}),
            'total_pages':forms.NumberInput(attrs={'class':'form-control'}),
            'year':forms.NumberInput(attrs={'class':'form-control'}),
            'review':forms.Textarea(attrs={'class':'form-control','rows':5})
        }#model form nn inherit cheythale  ith work aku.inputfield matre set cheyyullu

class RegistrationModelForm(forms.ModelForm):
    class Meta:
        model=User
        fields=["username","email","password"]

        widgets={
            'username':forms.TimeInput(attrs={'class':'form-control'}),
            'email':forms.EmailInput(attrs={'class':'form-control'}),
            'password':forms.PasswordInput(attrs={'class':'form-control'})
        }
#--------------------------------------------------------------------
class LoginForm(forms.Form):
    username=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    password=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'})) 