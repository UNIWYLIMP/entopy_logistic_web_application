from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

# Primary Models Initialization.


# User Profiles
class CustomUser(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
    username = models.CharField(_('User Name'), unique=True, max_length=250)
    fullname = models.CharField(_('Full Name'), default="", max_length=250)
    status = models.CharField(_('Status'), default="user", max_length=250)

    class Meta:
        db_table = 'Universal Profile'


class DeliveryCompany(models.Model):
    profile = models.ForeignKey('CustomUser', on_delete=models.CASCADE, default=1)
    email = models.EmailField(_('Company email address'), unique=True)
    username = models.CharField(_('Company User Name'), unique=True, max_length=250)
    fullname = models.CharField(_('Company Name'), default="", max_length=250)
    company_location = models.CharField(_("Company Location"), default="", max_length=1000)
    working_days = models.CharField(_("Working Days"), default="", max_length=250)
    policies = models.CharField(_("Delivery Policy"), default="", max_length=10000)

    class Meta:
        db_table = 'Company Profile'


class DeliveryDestination(models.Model):
    company = models.ForeignKey('DeliveryCompany', on_delete=models.CASCADE, default=1)
    one_country = models.CharField(_("Country"), default="", max_length=1000)
    one_cities = models.CharField(_("Cities"), default="", max_length=1000)
    two_country = models.CharField(_("Country"), default="", max_length=1000)
    two_cities = models.CharField(_("Cities"), default="", max_length=1000)
    mode_of_delivery = models.CharField(_("Mode Of Delivery"), default="", max_length=1000)
    rate = models.FloatField(_("Rate Per Kg"), default=0)


class Order(models.Model):
    product_name = models.CharField(_("Product Name"), default="", max_length=1000)
    product_description = models.CharField(_("Product Description"), default="", max_length=1000)
    amount_paid = models.FloatField(_("Payment"), default=0)
    weight = models.FloatField(_("Weight"), default=0)
    status = models.CharField(_("Status"), default="", max_length=1000)
    company = models.ForeignKey('DeliveryCompany', on_delete=models.CASCADE, default=1)
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE, default=1)
    created_at = models.DateTimeField(auto_now_add=True)
