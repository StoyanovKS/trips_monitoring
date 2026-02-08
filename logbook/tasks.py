from celery import shared_task
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.utils import timezone

from .models import Trip, Refuel

User = get_user_model()


@shared_task
def send_weekly_summary_email(user_id: int) -> bool:
    user = User.objects.filter(pk=user_id).first()
    if not user or not user.email:
        return False

    today = timezone.localdate()
    start = today - timezone.timedelta(days=7)

    trips = Trip.objects.filter(car__owner=user, start_date__gte=start, start_date__lte=today)
    refuels = Refuel.objects.filter(car__owner=user, date__gte=start, date__lte=today)

    trips_count = trips.count()
    total_km = sum((t.distance_km for t in trips), 0)

    refuels_count = refuels.count()
    total_cost = sum((r.total_cost for r in refuels), 0)

    subject = "Your weekly Trip Logbook summary"
    message = (
        f"Hi {user.username},\n\n"
        f"Weekly summary ({start} → {today}):\n"
        f"- Trips: {trips_count}\n"
        f"- Distance: {total_km} km\n"
        f"- Refuels: {refuels_count}\n"
        f"- Fuel cost: {total_cost}\n\n"
        f"Have a great week!\n"
    )

    send_mail(
        subject=subject,
        message=message,
        from_email=None, 
        recipient_list=[user.email],
        fail_silently=True,
    )
    return True


@shared_task
def send_weekly_summary_for_all_users() -> int:
    user_ids = list(User.objects.exclude(email="").exclude(email__isnull=True).values_list("id", flat=True))
    for uid in user_ids:
        send_weekly_summary_email.delay(uid)
    return len(user_ids)