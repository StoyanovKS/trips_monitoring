from django.contrib.auth import get_user_model

User = get_user_model()

def create_user(username="u1", password="StrongPass123!", email=None, **extra):
    if email is None:
        email = f"{username}@test.com"
    return User.objects.create_user(
        username=username,
        password=password,
        email=email,
        **extra,
    )
