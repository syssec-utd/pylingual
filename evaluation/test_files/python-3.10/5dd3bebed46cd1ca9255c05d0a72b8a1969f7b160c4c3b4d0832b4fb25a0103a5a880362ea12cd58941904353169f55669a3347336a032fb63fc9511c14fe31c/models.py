from django.db import models
from .enum import InterestRateTypeChoices

class Finance(models.Model):
    finance_date = models.DateTimeField(auto_now_add=True)
    finance_request_id = models.IntegerField(blank=True, null=True)
    program_type = models.CharField(max_length=255, blank=True, null=True)
    anchor_party = models.IntegerField(blank=True, null=True)
    counterparty = models.IntegerField(blank=True, null=True)
    due_date = models.DateField(blank=True, null=True)
    loan_account = models.CharField(max_length=255, blank=True, null=True)
    invoice_currency = models.CharField(max_length=255, blank=True, null=True)
    invoice_amount = models.IntegerField(blank=True, null=True)
    finance_currency = models.CharField(max_length=255, blank=True, null=True)
    finance_amount = models.IntegerField(blank=True, null=True)
    settlement_currency = models.CharField(max_length=255, blank=True, null=True)
    settlement_amount = models.IntegerField(blank=True, null=True)
    repayment_currency = models.CharField(max_length=255, blank=True, null=True)
    repayment_account = models.CharField(max_length=255, blank=True, null=True)
    interest_type = models.CharField(max_length=255, blank=True, null=True)
    interest_rate_type = models.CharField(max_length=255, blank=True, null=True)
    margin = models.FloatField(blank=True, null=True)
    interest_rate = models.FloatField(blank=True, null=True)
    interest_amount = models.IntegerField(blank=True, null=True)
    interest_paid_by = models.CharField(max_length=255, blank=True, null=True)
    own_party_account_info = models.JSONField(blank=True, null=True)
    remittance_info = models.JSONField(blank=True, null=True)
    status = models.CharField(max_length=255, blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)

class FinanceAccounting(models.Model):
    finance_model = models.ForeignKey(Finance, on_delete=models.CASCADE, related_name='finance_account', blank=True, null=True)
    contract_ref = models.CharField(max_length=155, blank=True, null=True)
    stage = models.CharField(max_length=155, blank=True, null=True)
    type = models.CharField(max_length=155, blank=True, null=True)
    currency = models.CharField(max_length=155, blank=True, null=True)
    amount = models.FloatField(blank=True, null=True)
    account = models.CharField(max_length=255, blank=True, null=True)
    interest_paid_by = models.CharField(max_length=255, blank=True, null=True)
    account_type = models.CharField(max_length=155, blank=True, null=True)
    base_currency = models.CharField(max_length=155, blank=True, null=True)
    base_currency_amount = models.IntegerField(blank=True, null=True)
    exch_rate = models.FloatField(blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.finance_model.id} - {self.type} - {self.interest_paid_by}'

class Exchangerate(models.Model):
    bank_entity = models.IntegerField(blank=True, null=True)
    rate_base_currency = models.CharField(max_length=255, blank=True, null=True)
    rate_currency = models.CharField(max_length=255, blank=True, null=True)
    rate_date = models.DateField(blank=True, null=True)
    rate_previous_day = models.DateField(blank=True, null=True)
    rate_buy = models.FloatField(blank=True, null=True)
    rate_sell = models.FloatField(blank=True, null=True)
    rate_mid = models.FloatField(blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.rate_currency} - {self.rate_mid}'

class Interestaccount(models.Model):
    bank_entity = models.CharField(max_length=255, blank=True, null=True)
    program_type = models.CharField(max_length=255, blank=True, null=True)
    currency = models.CharField(max_length=255, blank=True, null=True)
    account = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f'{self.program_type} - {self.currency}'

class Loanaccount(models.Model):
    bank_entity = models.CharField(max_length=255, blank=True, null=True)
    customer = models.CharField(max_length=255, blank=True, null=True)
    program_type = models.CharField(max_length=255, blank=True, null=True)
    currency = models.CharField(max_length=255, blank=True, null=True)
    account = models.CharField(max_length=255, blank=True, null=True)

class Currency(models.Model):
    description = models.CharField(max_length=10)
    days_in_year = models.IntegerField(blank=True, null=True)
    rounding_units = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.description

class FloatingInterestRate(models.Model):
    bank_entity = models.CharField(max_length=255, blank=True, null=True)
    rate_date = models.DateField(blank=True, null=True)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name='floating_currency', blank=True, null=True)
    interest_rate_type = models.CharField(max_length=255, choices=InterestRateTypeChoices.choices, blank=True, null=True)
    period = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f'{self.interest_rate_type} - {self.currency} '