from django.db import models
from django.utils import timezone
from django.contrib.auth.models import Group
import uuid

from django.conf import settings

# Create your models here.
class Company(models.Model):
    """
        A representation of a company. It contains the important information and is linked to a Django `Group`.
        Linking to the Django `Group` makes it possible to map `User` to a `Company`.
    """

    id = models.UUIDField(
        unique=True,
        primary_key=True,
        default=uuid.uuid4(),
        editable=False,
        blank=False,
        null=False,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    modified = models.DateTimeField(
        default=timezone.now,                   # 'auto_now_add' is not editable
    )
    name = models.CharField(
        max_length=80,
        default="Company XYZ",
        blank=False,
        null=False,
        help_text="The name of the company.",
    )
    description = models.TextField(
        blank=True,
        null=True,
        help_text="Description of the company.",
    )
    group = models.ForeignKey(
        Group,
        on_delete=models.DO_NOTHING,
        related_name='companygroup',
        blank=False,
        null=False,
        help_text="Which Django group this company is connected to.",
    )
    url = models.URLField(
        blank=True,
        null=True,
        help_text="(optional) Company URL field.",
    )
    active = models.BooleanField(
        default=True,
        help_text="If this company is active or not. When disabled, no account related to this company can login.",
    )

    class Meta:
        verbose_name = "Company"
        verbose_name_plural = "Companies"

    def __str__(self):
        return f"Company {self.name}"


class Billing(models.Model):
    """
        Billing information of a company is stored in this model. A separate model as multiple billing credentials are possible.
    """

    id = models.UUIDField(
        unique=True,
        primary_key=True,
        default=uuid.uuid4(),
        editable=False,
        blank=False,
        null=False,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    modified = models.DateTimeField(
        default=timezone.now,                   # 'auto_now_add' is not editable
    )
    code = models.UUIDField(
        unique=True,
        default=uuid.uuid4(),
        editable=False,
        blank=False,
        null=False,
        help_text="Unique billing code. Used to identify billing during support.",
    )
    name = models.CharField(
        max_length=80,
        default="main",
        blank=False,
        null=False,
        help_text="A name associated to this billing information.",
    )
    description = models.TextField(
        blank=True,
        null=True,
        help_text="Optional description of this billing information.",
    )
    company = models.ForeignKey(
        Company,
        on_delete=models.SET_NULL,
        related_name="billinginfocompany",
        null=True,
        help_text="Which company this billing information is connected to.",
    )
    old_company = models.CharField(
        max_length=80,
        blank=True,
        null=False,
        help_text="The name of the company. Used as backup for when the company were to be removed and we need to know where this subscription was from. <b>Will be overwritten automatically</b>.",
    )

    ###### ADD BILLING FIELDS HERE ######

    active = models.BooleanField(
        default=False,
        help_text="If this billing information is active or not.",
    )

    class Meta:
        verbose_name = "Billing record"
        verbose_name_plural = "Billing records"

    def __str__(self):
        return f"Billing record of {self.company}"

    def save(self, *args, **kwargs):
        """ Some additional settings when saving an entry of this model. """

        # Save company name during save
        self.old_company = self.company.name

        # Disabling other billing methods as only one can be active
        if self.active:
            try:
                currentactive = Billing.objects.get(company=self.company, active=True)
                if self != currentactive:
                    currentactive.active = False
                    currentactive.save()
            except Billing.DoesNotExist:
                pass
        super(Billing, self).save(*args, **kwargs)


class Subscription(models.Model):
    """
        `Subscription` contains tokens and trial related information of a `Company`. A separate model as multiple subscriptions are possible.
    """

    SUBSCRIPTION_TYPES =  ((x, x) for x in settings.SUBSCRIPTIONS.keys())

    id = models.UUIDField(
        unique=True,
        primary_key=True,
        default=uuid.uuid4(),
        editable=False,
        blank=False,
        null=False,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    modified = models.DateTimeField(
        default=timezone.now,                   # 'auto_now_add' is not editable
    )
    code = models.UUIDField(
        unique=True,
        default=uuid.uuid4(),
        editable=False,
        blank=False,
        null=False,
        help_text="Unique subscription code. Used to identify subscription during support.",
    )
    name = models.CharField(
        max_length=80,
        default="main",
        blank=False,
        null=False,
        help_text="A name associated to this billing information.",
    )
    description = models.TextField(
        blank=True,
        null=True,
        help_text="Optional description of this billing method.",
    )
    company = models.ForeignKey(
        Company,
        on_delete=models.SET_NULL,
        related_name="subscriptioncompany",
        null=True,
        help_text="Which company this subscription is connected to.",
    )
    old_company = models.CharField(
        max_length=80,
        blank=True,
        null=False,
        help_text="The name of the company. Used as backup for when the company were to be removed and we need to know where this subscription was from. <br><b>Will be overwritten automatically</b>.",
    )
    subscription = models.CharField(
        max_length=60,
        choices=SUBSCRIPTION_TYPES,
        default="none",
        help_text="The type of the subscription. Fields below will be used differently based on the selected subscription.",
    )
    monthly_tokens = models.FloatField(
        default=0,
        blank=False,
        null=False,
        help_text="Amount of monthly tokens. <b>Used for monthly subscriptions</b>.",
    )
    total_tokens_bought = models.FloatField(
        default=0,
        blank=False,
        null=False,
        help_text="Total amount of tokens bought, <b>incremented only at each topup</b>. <br><i>Used only for token-based subscriptions</i>.",
    )
    tokens = models.FloatField(
        default=0,
        blank=False,
        null=False,
        help_text="Current amount of tokens for this subscription. <b>Will only be reset when no tokens left and a topup is bought</b>. <br><i>Used only for token-based subscriptions</i>.",
    )
    trial_since = models.DateTimeField(
        default=timezone.now,                   # 'auto_now_add' is not editable
        help_text="Trial start date. <b>Used only for trial subscriptions</b>.",
    )
    trial_days = models.IntegerField(
        blank=False,
        null=False,
        default=0,
        help_text="Amount of days the trial should last. <b>Used only for trial subscriptions</b>.",
    )
    active = models.BooleanField(
        default=False,
        help_text="If this subscription is active or not.",
    )
    hidden = models.BooleanField(
        default=False,
        help_text="If this subscription should be hidden from the customer. Used to 'remove' old subscriptions which are still useful for subscription/billing management.",
    )

    class Meta:
        verbose_name = "Subscription"
        verbose_name_plural = "Subscriptions"

    def __str__(self):
        return f"Subscription of {self.company}"

    def save(self, *args, **kwargs):
        """ Some additional settings when saving an entry of this model. """

        # Save company name during save
        self.old_company = self.company.name

        # Disabling other subscriptions as only one can be active
        if self.active:
            try:
                currentactive = Subscription.objects.get(company=self.company, active=True)
                if self != currentactive:
                    currentactive.active = False
                    currentactive.save()
            except Subscription.DoesNotExist:
                pass
        super(Subscription, self).save(*args, **kwargs)
