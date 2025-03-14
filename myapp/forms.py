from django import forms
from myapp.models import TaskModel

class User_form(forms.Form):
    
    username=forms.CharField(max_length=100,widget=forms.TextInput(attrs={"class":"form-control ","placeholder":"Enter Username"}))

    first_name=forms.CharField(max_length=100,widget=forms.TextInput(attrs={"class":"form-control ","placeholder":"Enter Firstname"}))

    last_name=forms.CharField(max_length=100,widget=forms.TextInput(attrs={"class":"form-control","placeholder":"Enter Lastname"}))

    password=forms.CharField(max_length=100,widget=forms.PasswordInput(attrs={"class":"form-control","placeholder":"Enter Password"}))

    email=forms.EmailField(max_length=100,widget=forms.EmailInput(attrs={"class":"form-control","placeholder":"Enter E-mail"}))



class Login_form(forms.Form):
    username=forms.CharField(max_length=200,widget=forms.TextInput(attrs={"class":"form-control","placeholder":"Enter Username"}))
    
    password=forms.CharField(max_length=100,widget=forms.PasswordInput(attrs={"class":"form-control","placeholder":"Enter Password"}))


class Taskform(forms.ModelForm):

   class Meta:
       
       model=TaskModel

       fields=["task_name","due_date","priority_level"]
   
