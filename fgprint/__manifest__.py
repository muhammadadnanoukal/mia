# -*- coding: utf-8 -*-
###################################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#    Copyright (C) 2021-TODAY Cybrosys Technologies(<http://www.cybrosys.com>).
#    Author: cybrosys(<https://www.cybrosys.com>)
#
#    This program is free software: you can modify
#    it under the terms of the GNU Affero General Public License (AGPL) as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
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
    'name': 'Altanmya fingerprint adaptor 5',
    'version': '5',
    'summary': 'Serve for attendance',
    'description': """Flexable module to handle attendance and payroll""",
    'category': 'Human Resources/Employees',
    'author': 'Altanmia co.',
    'company': 'Altanmia',
    'website': "https://www.altanmya.net",
    'depends': ['hr','resource','hr_attendance','hr_contract','hr_payroll'],
    'data': ['security/ir.model.access.csv','views/tstyle.xml','views/view_actions.xml','views/view_menu.xml','views/view_v.xml','data/data.xml'],
    'demo': [],
    'qweb': [],
    'installable': True,
    'auto_install': False,
    'application': True,
}
