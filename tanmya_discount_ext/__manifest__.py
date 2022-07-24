{
    'name': 'Tanmya Discount extension',
    'version': '1.0',
    'summary': 'Additional Discount feature for purchase & invoicing modules',
    'description': "",
    'category': 'Inventory/Purchase',
    'author': 'Tanmya co.',
    'company': 'Tanmya',
    'website': "https://www.altanmya.net",
    'depends': ['purchase','account'],
    'data': [
        'views/tanmya_purchase_views.xml',
        'views/tanmya_account_views.xml'
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}