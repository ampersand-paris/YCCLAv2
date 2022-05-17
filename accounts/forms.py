from django import forms 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate

from accounts.models import CustomUser, RecipeCollection

class RegistrationForm(UserCreationForm):

    email = forms.EmailField(max_length=255, help_text="Required. Add a valid email address.")

    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        try:
            account = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
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

class AccountUpdateForm(forms.ModelForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'fname', 'lname', 'bio')

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        try:
            account = CustomUser.objects.exclude(pk=self.instance.pk).get(email=email)
        except CustomUser.DoesNotExist:
            return email
        raise forms.ValidationError(f"Email {email} is already in use.")

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            username = CustomUser.objects.exclude(pk=self.instance.pk).get(username=username)
        except CustomUser.DoesNotExist:
            return username
        raise forms.ValidationError(f"Username {username} is already in use.")

    def save(self, commit=True):
        account = super(AccountUpdateForm, self).save(commit=False)
        account.username = self.cleaned_data['username']
        account.email = self.cleaned_data['email'].lower()
        account.fname = self.cleaned_data['fname']
        account.lname = self.cleaned_data['lname']
        account.bio = self.cleaned_data['bio']
        if commit:
            account.save()
        return account

class RecipeCollectionCreate(forms.ModelForm):

    class Meta:
        model = RecipeCollection
        fields = ('recipe', 'sent', 'sent_to', 'received', 'received_from', 'user')

class RecipeCollectionUpdateForm(forms.ModelForm):

    class Meta:
        model = RecipeCollection
        fields = ('sent', 'sent_to', 'received', 'received_from')

    def save(self, commit=True):
        collection = super(RecipeCollectionUpdateForm, self).save(commit=False)
        collection.sent = self.cleaned_data['sent']
        collection.sent_to = self.cleaned_data['sent_to']
        collection.received = self.cleaned_data['received']
        collection.received_from = self.cleaned_data['received_from']

        if commit:
            print('form save')
            collection.save()
        return collection