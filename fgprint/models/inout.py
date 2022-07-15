from odoo import api,models, fields

class Inout(models.Model):
      _name = 'od.inout'
      _description = 'Attendance table'

      emp_deviceno = fields.Integer(string='employee id device')
      emp_name=fields.Char(string='Employee name',compute='_getname',depends=['emp_deviceno'],store=False)
      date_in = fields.Datetime(string='time in')
      date_out = fields.Datetime(string='time out')
      shift_id = fields.Many2one('resource.calendar.attendance',string='shift')
      date_inflag =fields.Selection([('internal','Internal'),('setting','Setting'),('manuel','Manuel')],string='date in source', default='manuel')
      date_outflag = fields.Selection([('internal','Internal'),('setting','Setting'),('manuel','Manuel')],string='date out source', default='manuel')
      att_date=fields.Datetime(string='Attendance date')

      def _getname(self):
            for inout_rec in self:
                  rec=self.env['hr.employee'].search([('studio_employee_number','=',inout_rec.emp_deviceno)])
                  if rec:
                   if len(rec)==1:
                     inout_rec.emp_name=rec.display_name
                   else:
                     inout_rec.emp_name = 'TOO MANY EMP!!'
                  else:
                   inout_rec.emp_name = 'NOT DEFINED!!'




