from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

User = get_user_model()


class RegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email", "preferred_currency", "timezone")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["username"].label = "User Name"
        self.fields["email"].label = "Email"

        self.fields["username"].widget.attrs.update({"placeholder": "username_@!1"})
        self.fields["email"].widget.attrs.update({"placeholder": "put_your_name@example.com"})
        self.fields["preferred_currency"].label = "Currency"
        self.fields["timezone"].label = "Timezone"

        # По-приятни текстове за пароли
        self.fields["password1"].label = "Enter your Password"
        self.fields["password2"].label = "Please repeat your password"
        self.fields["password1"].help_text = ""
        self.fields["password2"].help_text = ""

        self.error_messages["password_mismatch"] = "Passwords do not match!"


class LoginForm(AuthenticationForm):
    
    username = forms.CharField(
        label="User name",
        widget=forms.TextInput(attrs={"placeholder": "User name"}),
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={"placeholder": "Password"}),
    )

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("email", "preferred_currency", "timezone")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["email"].label = "Email"
        self.fields["preferred_currency"].label = "Currency"
        self.fields["timezone"].label = "Timezone"

        self.fields["email"].widget.attrs.update({"placeholder": "email"})
        self.fields["timezone"].widget.attrs.update({"placeholder": "Europe/Sofia"})

        # Disabled/read-only requirement #1
        self.fields["email"].disabled = True