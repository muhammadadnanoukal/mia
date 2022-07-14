# -*- coding: utf-8 -*-
###################################################################################
#
#    ALTANMYA - TECHNOLOGY SOLUTIONS
#    Copyright (C) 2022-TODAY ALTANMYA - TECHNOLOGY SOLUTIONS Part of ALTANMYA GROUP.
#    ALTANMYA - Last Purchase Price Per Product in Purchasing Module.
#    Author: ALTANMYA for Technology(<https://tech.altanmya.net>)
#
#    This program is Licensed software: you can not modify
#   #
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###################################################################################
{
    'name': 'Purchase Last Price',
    'version': '1.0',
    'category': 'Inventory/Purchase',
    'summary': 'Retrive the Last Purchase Price Per Product in Purchasing Module',
    'author': 'ALTANMYA - TECHNOLOGY SOLUTIONS',
    'company': 'ALTANMYA - TECHNOLOGY SOLUTIONS Part of ALTANMYA GROUP',
    'website': "https://tech.altanmya.net",
    'summary': 'Product Last Purchased Price',
    'depends': ['purchase'],
    'data': [
        'views/last_price_field.xml'
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
    'license': 'LGPL-3',
}