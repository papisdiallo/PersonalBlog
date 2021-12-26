from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model, authenticate
from .models import Profile
from django.contrib.auth.forms import PasswordResetForm

User = get_user_model()
            
class LoginForm(forms.Form):
    Username_or_Email = forms.CharField(max_length=140, widget=forms.TextInput(attrs={
    }))
    Password = forms.CharField(widget=forms.PasswordInput())

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get('Username_or_Email')
        password = self.cleaned_data.get('Password')
        if not username:
            raise forms.ValidationError("You have to provide a username or email")
        if not password:
            raise forms.ValidationError("You must enter your password")
        else:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError("Something went wrong with your credentials. Please try again")
        return super(LoginForm, self).clean(*args, **kwargs)




class CostumUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email',)
   
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if '@' in username:
            raise forms.ValidationError(" '@' is not a allowed character for this field. Please try again")
        return username


class UserRegistrationForm(CostumUserCreationForm):

    class Meta:
        model = User
        fields = ['email', 'username', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if '@' in username:
            raise forms.ValidationError(" '@' is not a allowed character for this field. Please try again")
        return username 

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_picture', 'city', 'profession']

 