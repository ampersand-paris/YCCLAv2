from django import forms 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate

from accounts.models import CustomUser

class RegistrationForm(UserCreationForm):

    email = forms.EmailField(max_length=255, help_text="Required. Add a valid email address.")

    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        try:
            account = CustomUser.objects.get(email=email)
        except Exception as e:
            return email
        raise forms.ValidationError(f"Email {email} is already in use.")

    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        try:
            username = CustomUser.objects.get(username=username)
        except Exception as e:
            return username
        raise forms.ValidationError(f"Email {username} is already in use.")
    
class AccountAuthenticationForm(forms.ModelForm):

	password = forms.CharField(label='Password', widget=forms.PasswordInput)

	class Meta:
		model = CustomUser
		fields = ('email', 'password')

	def clean(self):
		if self.is_valid():
			email = self.cleaned_data['email']
			password = self.cleaned_data['password']
			if not authenticate(email=email, password=password):
				raise forms.ValidationError("Invalid login")
