from django.db import models
from django.contrib.auth.models import User
from django_extensions.db.models import TimeStampedModel


class Config(TimeStampedModel):
    config_key = models.CharField(max_length=255)
    config_value = models.CharField(max_length=255)

    class Meta:
        app_label = "parking"
        verbose_name = "Config"
        verbose_name_plural = "Configs"

    def __init__(self, *args, **kwargs):
        super(Config, self).__init__(*args, **kwargs)

    def __str__(self):
        return "Config %s" % self.config_key


class Transaction(TimeStampedModel):
    ENTRY = 1
    EXIT = 2
    QUEUE = 3
    PARKING_CHOICES = (
        (ENTRY, 'Entry'),
        (EXIT, 'Exit'),
        (QUEUE, 'Queue'),
    )

    car_number = models.CharField(max_length=25)
    parking_status = models.PositiveSmallIntegerField(choices=PARKING_CHOICES)
    entry_date = models.DateTimeField(default=None, blank=True, null=True)
    exit_date = models.DateTimeField(default=None, blank=True, null=True)
    created_user = models.ForeignKey(User, related_name='created_user', default=None, blank=True, null=True,
                                     on_delete=models.CASCADE)
    modified_user = models.ForeignKey(User, related_name='modified_user', default=None, blank=True, null=True,
                                      on_delete=models.CASCADE)

    class Meta:
        app_label = "parking"
        verbose_name = "Transaction"
        verbose_name_plural = "Transactions"

    def __init__(self, *args, **kwargs):
        super(Transaction, self).__init__(*args, **kwargs)

    def __str__(self):
        return "Transaction %s" % self.car_number
