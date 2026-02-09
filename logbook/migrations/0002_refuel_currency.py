from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("logbook", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="refuel",
            name="currency",
            field=models.CharField(
                choices=[("BGN", "BGN"), ("EUR", "EUR")],
                default="BGN",
                help_text="Currency of the total cost.",
                max_length=3,
            ),
        ),
    ]
