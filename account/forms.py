from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Account


class UserRegistrationForm(UserCreationForm):

	username = forms.CharField(widget=forms.TextInput(attrs={
		'class': 'form-control',
		'id': 'username'
		}))

	password1 = forms.CharField(widget=forms.PasswordInput(attrs={
		'class': 'form-control',
		'id': 'password'
		}))

	password2 = forms.CharField(widget=forms.PasswordInput(attrs={
		'class': 'form-control',
		'id': 'confirm-password'
		}))

	email = forms.CharField(widget=forms.EmailInput(attrs={
		'class': 'form-control',
		'id': 'email'
		}))

	first_name = forms.CharField(widget=forms.TextInput(attrs={
		'class': 'form-control',
		'id': 'first_name'
		}))

	last_name = forms.CharField(widget=forms.TextInput(attrs={
		'class': 'form-control',
		'id': 'last_name'
		}))

	class Meta:
		model = Account
		fields = ['email', 'username', 'first_name', 'last_name', 'password1', 'password2']

class AccountUpdationForm(forms.ModelForm):

	username = forms.CharField(widget=forms.TextInput(attrs={
		'class': 'form-control',
		'id': 'username'
		}))

	email = forms.CharField(widget=forms.EmailInput(attrs={
		'class': 'form-control',
		'id': 'email'
		}))

	first_name = forms.CharField(widget=forms.TextInput(attrs={
		'class': 'form-control',
		'id': 'first_name'
		}))

	last_name = forms.CharField(widget=forms.TextInput(attrs={
		'class': 'form-control',
		'id': 'last_name'
		}))

	class Meta:
		model = Account
		fields = ['email', 'username', 'first_name', 'last_name','profile_pic' ]

	def clean_email(self):
		email = self.cleaned_data['email']

		try:
			emails = Account.objects.exclude(pk=self.instance.pk).get(email=email)

		except Account.DoesNotExist:
			return email		

		raise forms.ValidationError('Email is already in use.')
		

	def clean_username(self):
		username = self.cleaned_data['username']

		try:
			usernames = Account.objects.exclude(pk=self.instance.pk).get(username=username)

		except Account.DoesNotExist:
			return username

		raise forms.ValidationError('Username is already in use.')

	

