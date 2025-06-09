import datetime as dt
import pytest
from cuenca_validations.types import EntryType, SavingCategory, TransactionStatus, WalletTransactionType
from cuenca import BalanceEntry, Saving, WalletTransaction

@pytest.mark.vcr
def test_create_wallet_transaction():
    wallet_id = 'LAvWUDH6OpQk-ber3E_zUEiQ'
    deposit = WalletTransaction.create(wallet_uri=f'/savings/{wallet_id}', transaction_type=WalletTransactionType.deposit, amount=10000)
    assert deposit.id is not None
    assert deposit.transaction_type == WalletTransactionType.deposit
    assert deposit.status == TransactionStatus.succeeded
    wallet = deposit.wallet
    assert wallet.id == wallet_id

@pytest.mark.vcr
def test_retrieve_wallet_transaction():
    id = 'LT32GEaFQR03cJRBcqb0p7uI'
    transaction = WalletTransaction.retrieve(id)
    assert transaction.id == id
    assert transaction.status == TransactionStatus.succeeded

@pytest.mark.vcr
def test_query_wallet_transactions():
    wallet_uri = '/savings/LAGdf-FVVeQeeKrmYpF5NIfA'
    query = WalletTransaction.all(wallet_uri=wallet_uri)
    transactions = [txn for txn in query]
    assert len(transactions) == 2

@pytest.mark.vcr
def test_complete_flow_wallets():
    saving = Saving.create(name='Ahorros', category=SavingCategory.travel, goal_amount=1000000, goal_date=dt.datetime.now() + dt.timedelta(days=365))
    assert saving.balance == 0
    assert saving.wallet_uri == f'/savings/{saving.id}'
    deposit = WalletTransaction.create(wallet_uri=saving.wallet_uri, transaction_type=WalletTransactionType.deposit, amount=10000)
    assert deposit.status == TransactionStatus.succeeded
    saving.refresh()
    assert saving.balance == deposit.amount
    deposit_uri = f'/wallet_transactions/{deposit.id}'
    withdrawal = WalletTransaction.create(wallet_uri=saving.wallet_uri, transaction_type=WalletTransactionType.withdrawal, amount=2000)
    assert withdrawal.status == TransactionStatus.succeeded
    saving.refresh()
    assert saving.balance == deposit.amount - withdrawal.amount
    withdrawal_uri = f'/wallet_transactions/{withdrawal.id}'
    query = WalletTransaction.all(wallet_uri=saving.wallet_uri)
    transactions_db = [wt.id for wt in query]
    assert deposit.id in transactions_db
    assert withdrawal.id in transactions_db
    entries = BalanceEntry.all(wallet_id=saving.id)
    wallet_entries = [entry for entry in entries]
    assert len(wallet_entries) == 2
    credit = [be for be in wallet_entries if be.type == EntryType.credit][0]
    assert credit.related_transaction_uri == deposit_uri
    assert credit.amount == deposit.amount
    debit = [be for be in wallet_entries if be.type == EntryType.debit][0]
    assert debit.amount == withdrawal.amount
    assert debit.related_transaction_uri == withdrawal_uri
    entries = BalanceEntry.all(wallet_id='default', funding_instrument_uri=saving.wallet_uri)
    default_entries = [entry for entry in entries]
    assert len(default_entries) == 2
    debit = [be for be in default_entries if be.type == EntryType.debit][0]
    assert debit.related_transaction_uri == deposit_uri
    assert debit.amount == deposit.amount
    credit = [be for be in default_entries if be.type == EntryType.credit][0]
    assert credit.amount == withdrawal.amount
    assert credit.related_transaction_uri == withdrawal_uri