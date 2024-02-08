from django.urls import re_path
from .views import *


urlpatterns = [
    re_path('transaction/detail/', TransactionDetailView.as_view(), name='transaction detail'),
    re_path('transaction/entry/', TransactionEntryView.as_view(), name='transaction entry'),
    re_path('transaction/exit/', TransactionExitView.as_view(), name='transaction exit'),
    re_path('reporting/', ReportingView.as_view(), name='parking reporting'),
]