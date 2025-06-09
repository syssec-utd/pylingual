from openupgradelib import openupgrade

def migrate(cr, installed_version):
    openupgrade.load_data(cr, 'l10n_it_withholding_tax', 'migrations/13.0.1.0.0/noupdate_changes.xml')
    openupgrade.logged_query(cr, '\nupdate account_move\nset\n    withholding_tax = inv.withholding_tax,\n    withholding_tax_amount = inv.withholding_tax_amount,\n    amount_net_pay = inv.amount_net_pay,\n    amount_net_pay_residual = inv.amount_net_pay_residual\nfrom account_invoice inv\nwhere\n    account_move.id = inv.move_id;\n    ')
    openupgrade.logged_query(cr, '\nupdate account_invoice_withholding_tax\nset\n    invoice_id = am.id\nfrom account_invoice inv\n    join account_move am on am.id = inv.move_id\nwhere\n    invoice_id = inv.id;\n    ')