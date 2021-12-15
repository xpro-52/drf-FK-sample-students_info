from django.db import models
from django.utils.translation import gettext_lazy as _


class Department(models.Model):
    name = models.CharField(_("Name"), max_length=128)

    def __str__(self) -> str:
        return self.name


class Student(models.Model):
    first_name = models.CharField(_("first name"), max_length=64)
    last_name = models.CharField(_("last name"), max_length=64)
    department = models.ForeignKey(to=Department, on_delete=models.CASCADE)

    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name

    def __str__(self) -> str:
        return self.get_full_name()


