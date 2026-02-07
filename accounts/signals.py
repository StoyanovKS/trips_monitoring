from django.apps import apps
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.core.mail import send_mail
from django.db.models.signals import post_migrate, post_save
from django.dispatch import receiver

User = get_user_model()


@receiver(post_migrate)
def create_groups_and_permissions(sender, **kwargs):
    """
    Creates required groups and assigns permissions after migrations.

    This runs after every migrate, but is idempotent:
    - Groups are created if missing
    - Permissions are added if missing
    """
    if sender.name != "accounts":
        return

    drivers_group, _ = Group.objects.get_or_create(name="Drivers")
    managers_group, _ = Group.objects.get_or_create(name="Managers")

    # Expand Drivers a bit (still safe because ownership is enforced in views/querysets)
    permission_map = {
        "Drivers": [
            ("garage", "car", ["add", "change", "view"]),
            ("logbook", "trip", ["add", "change", "view"]),
            ("logbook", "refuel", ["add", "change", "view"]),
            ("logbook", "tag", ["view"]),
        ],
        "Managers": [
            ("garage", "car", ["add", "change", "delete", "view"]),
            ("logbook", "trip", ["add", "change", "delete", "view"]),
            ("logbook", "refuel", ["add", "change", "delete", "view"]),
            ("logbook", "tag", ["add", "change", "delete", "view"]),
        ],
    }

    groups = {
        "Drivers": drivers_group,
        "Managers": managers_group,
    }

    for group_name, rules in permission_map.items():
        group = groups[group_name]

        for app_label, model_name, actions in rules:
            model = apps.get_model(app_label, model_name)
            if model is None:
                continue

            for action in actions:
                codename = f"{action}_{model._meta.model_name}"
                try:
                    perm = Permission.objects.get(
                        content_type__app_label=app_label,
                        codename=codename,
                    )
                except Permission.DoesNotExist:
                    continue

                group.permissions.add(perm)


@receiver(post_save, sender=User)
def assign_default_group_and_send_email(sender, instance, created, **kwargs):
    """
    On registration:
    1) Add user to Drivers group by default (prevents 'empty user' with no role).
    2) Send a welcome email (in dev it goes to console backend).
    """
    if not created:
        return

    # Default group assignment
    drivers_group, _ = Group.objects.get_or_create(name="Drivers")
    instance.groups.add(drivers_group)

    # Welcome email (only if email is provided)
    if instance.email:
        subject = "Welcome to Trips Monitoring"
        message = (
            f"Hi {instance.username},\n\n"
            "Thanks for registering in Trips Monitoring.\n"
            "You can now log in, add your cars, track trips and refuels, and generate reports.\n\n"
            "Have a great day!"
        )
        from_email = getattr(settings, "DEFAULT_FROM_EMAIL", None) or "noreply@example.com"

        # Fail silently so registration never breaks if SMTP isn't configured.
        send_mail(subject, message, from_email, [instance.email], fail_silently=True)
