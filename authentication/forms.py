from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username',
                  'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['autofocus'] = False
        self.fields['first_name'].widget.attrs['required'] = True
        self.fields['last_name'].widget.attrs['required'] = True
        self.fields['email'].widget.attrs['required'] = True

    def clean(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if User.objects.filter(email=email).exists():
            raise ValidationError("Email Already exists")
        elif User.objects.filter(username=username).exists():
            raise ValidationError("Username Already exists")
        return self.cleaned_data


class ChangeUserForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username',
                  'email']

    def clean(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        # check if the email/username that is being submitted is not the current user email/username
        user = User.objects.get(username=self.initial['username'])
        user_of_email = User.objects.get(email=self.initial['email'])

        if User.objects.filter(username=username).exists() and user.username != username:
            raise ValidationError("Username Already exists")
        elif User.objects.filter(email=email).exists() and email != user.email:
            raise ValidationError("Email Already exists")

        return self.cleaned_data
