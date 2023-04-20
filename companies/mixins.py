from django.contrib.auth.mixins import UserPassesTestMixin

from .models import Company


class UserAllowedAccessMixin(UserPassesTestMixin):
    company = None

    def dispatch(self, request, *args, **kwargs):
        self.company = Company.objects.get(id=kwargs["pk"])
        return super().dispatch(request, *args, **kwargs)

    def test_func(self):
        if not self.company.approved:
            return (
                self.company.submitted_by == self.request.user
                or self.request.user.is_superuser
            )
        return True
