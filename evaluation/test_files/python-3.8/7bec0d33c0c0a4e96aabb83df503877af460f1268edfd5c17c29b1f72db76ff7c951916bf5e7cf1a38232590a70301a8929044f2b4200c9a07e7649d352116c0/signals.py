from django.dispatch import Signal
portfolios_grant_initiated = Signal()
portfolio_grant_accepted = Signal()
portfolio_grant_denied = Signal()
portfolios_request_initiated = Signal()
portfolio_request_accepted = Signal()
portfolio_request_denied = Signal()