from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied


class OwnerQuerySetMixin(LoginRequiredMixin):

    owner_field = "owner" 

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(**{self.owner_field: self.request.user})


class CreatedByQuerySetMixin(LoginRequiredMixin):

    created_by_field = "created_by"

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(**{self.created_by_field: self.request.user})