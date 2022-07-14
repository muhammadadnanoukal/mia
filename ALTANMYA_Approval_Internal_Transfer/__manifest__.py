# -*- coding: utf-8 -*-
###################################################################################
#
#    ALTANMYA - TECHNOLOGY SOLUTIONS
#    Copyright (C) 2022-TODAY ALTANMYA - TECHNOLOGY SOLUTIONS Part of ALTANMYA GROUP.
#    ALTANMYA Attendance Device Adaptor.
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
    'name': 'ALTANMYA Internal Transfer Approvals',
    'version': '1.0',
    'summary': 'Enable Users from Creation the Internal Transfer From Approval Application',
    'description': "Add a new approval type 'Create Transfer Request'",
    'category': 'Human Resources/Approvals',
    'author': 'ALTANMYA - TECHNOLOGY SOLUTIONS',
    'company': 'ALTANMYA - TECHNOLOGY SOLUTIONS Part of ALTANMYA GROUP',
    'website': "https://tech.altanmya.net",
    'depends': ['approvals', 'stock', 'product'],
    'data': ['security/ir.model.access.csv','views/transfer_approval_category_views.xml',
             'views/transfer_approval_product_line_views.xml','views/transfer_approval_request_views.xml'],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': False,
}