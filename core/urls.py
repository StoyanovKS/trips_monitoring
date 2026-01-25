from django.urls import path
from .views import HomeView, DashboardView

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    path("about/", TemplateView.as_view(template_name="core/about.html"), name="about"),
    path("features/", TemplateView.as_view(template_name="core/features.html"), name="features"),
    path("demo/", TemplateView.as_view(template_name="core/demo.html"), name="demo"),
]




