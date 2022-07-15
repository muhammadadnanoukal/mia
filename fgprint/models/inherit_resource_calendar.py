from odoo import api, models, fields

class ExtendResourceCal(models.Model):
    _inherit = 'resource.calendar'
    late_enter = fields.Integer(string='Late enter')
    # Todo
    # late_enter2 = fields.Integer(string='Late enter 2')
    early_exit = fields.Integer(string='Early exit')
    early_overtime = fields.Integer(string='Early overtime')
    overtime1 = fields.Integer(string='Overtime1')
    overtime2 = fields.Integer(string='Overtime2')
    work_shift = fields.Selection([('oneweek', 'One week'), ('twoweek', 'Two weeks'), ('flex', 'Flexible')], string='Work shift mode'
                                  ,default='oneweek')

class tanExtendShift(models.Model):
    _inherit = 'resource.calendar.attendance'
    tol_in_early = fields.Integer(string='Early in delay')
    tol_in_late = fields.Integer(string='Late in delay')
    tol_out_early = fields.Integer(string='Early out delay')
    tol_out_over = fields.Integer(string='Late out delay')