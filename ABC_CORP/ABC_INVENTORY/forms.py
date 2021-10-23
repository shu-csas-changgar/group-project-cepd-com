from django.contrib.auth.forms import UserCreationForm
from .models import User

class CreateUserForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['firstName', 'lastName', 'email', 'phone','address','officeLocation','password1', 'password2']

