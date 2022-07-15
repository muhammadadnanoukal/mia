{
    'name': 'Tanmya Purchase Smart Button',
    'version': '1.0',
    'summary': 'Purchase approvals bind',
    'description': "",
    'category': 'Inventory/Purchase',
    'author': 'Tanmya co.',
    'company': 'Tanmya',
    'website': "https://www.altanmya.net",
    'depends': ['purchase', 'approvals', 'approvals_purchase'],
    'data': [
             'views/purchase_form_view.xml',
             'views/approval_purchase_views.xml',
             'views/approval_category_views.xml',
             ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
