from django.apps import apps
from django.contrib.auth.models import Group, Permission
from django.db.models.signals import post_migrate
from django.dispatch import receiver


@receiver(post_migrate)
def create_groups_and_permissions(sender, **kwargs):
    """
    Creates required groups and assigns permissions after migrations.

    This runs after every migrate, but is idempotent:
    - Groups are created if missing
    - Permissions are added if missing
    """
    # Ensure we run this only once for our app (optional, but prevents noise)
    if sender.name != "accounts":
        return

    drivers_group, _ = Group.objects.get_or_create(name="Drivers")
    managers_group, _ = Group.objects.get_or_create(name="Managers")

    # Permission rules:
    # - Drivers: can add/change Trip & Refuel
    # - Managers: can add/change/delete Trip & Refuel, and manage Cars
    # (You can adjust later, but this is clearly different)

    permission_map = {
        "Drivers": [
            ("logbook", "trip", ["add", "change", "view"]),
            ("logbook", "refuel", ["add", "change", "view"]),
        ],
        "Managers": [
            ("garage", "car", ["add", "change", "delete", "view"]),
            ("logbook", "trip", ["add", "change", "delete", "view"]),
            ("logbook", "refuel", ["add", "change", "delete", "view"]),
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
                    # If permissions don't exist yet (model not migrated), skip safely
                    continue

                group.permissions.add(perm)
