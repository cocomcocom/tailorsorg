from django import forms

#your form here

class Enqueueform(forms.Form):

    Name = forms.CharField(label="Name", max_length=100)

    Dressid = forms.CharField(label="Dress id", max_length=10)

    Email = forms.CharField(label="Email", max_length=100)


class Loginform(forms.Form):

    template_name_label = None

    User_widget = forms.TextInput(attrs = {"class":"username", "placeholder":"Username"})

    Username = forms.CharField(widget = User_widget, label=None, max_length=100)

    Password_widget = forms.PasswordInput(attrs = {"class":"password", "placeholder":"Password"})

    Password = forms.CharField(widget = Password_widget, label=None, max_length=100)
    
