from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

User = get_user_model()


class RegisterForm(UserCreationForm):
    """
    Регистрация с user-friendly labels + placeholders.
    """
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email", "preferred_currency", "timezone")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["username"].label = "Потребителско име"
        self.fields["email"].label = "Имейл"

        self.fields["username"].widget.attrs.update({"placeholder": "напр. krasen123"})
        self.fields["email"].widget.attrs.update({"placeholder": "name@example.com"})
        self.fields["preferred_currency"].label = "Валута"
        self.fields["timezone"].label = "Часова зона"

        # По-приятни текстове за пароли
        self.fields["password1"].label = "Парола"
        self.fields["password2"].label = "Повтори паролата"
        self.fields["password1"].help_text = ""
        self.fields["password2"].help_text = ""

        self.error_messages["password_mismatch"] = "Паролите не съвпадат."


class LoginForm(AuthenticationForm):
    """
    Не е задължително, но е удобно за placeholders и по-хубави messages.
    """
    username = forms.CharField(
        label="Потребителско име",
        widget=forms.TextInput(attrs={"placeholder": "Потребителско име"}),
    )
    password = forms.CharField(
        label="Парола",
        widget=forms.PasswordInput(attrs={"placeholder": "Парола"}),
    )
