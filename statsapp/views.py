from django.views.generic import TemplateView

class MonthlyReportView(TemplateView):
    template_name = "statsapp/monthly_report.html"
