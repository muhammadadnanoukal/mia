from odoo import api,models, fields
from datetime import datetime, timedelta
from odoo.exceptions import UserError,Warning
import pytz

class AttPayRoll(models.Model):
      _name = 'od.attpayroll'
      _description = 'prepare for payroll'

      employee_id = fields.Many2one('hr.employee',string='Employee name', readonly=True)
      inout=fields.Integer('Reference Id')
      date_in = fields.Datetime(string='time in')
      diff_entry = fields.Char(string='Enter', readonly=True)

      date_out = fields.Datetime(string='time out')
      diff_Exit =fields.Char(string='Exit', readonly=True)

      status =fields.Selection([('draft', 'Draft'), ('validate', 'Validate'), ('reject', 'Reject'),('done', 'Done')],default='draft')
      status2 =fields.Selection([('draft', 'Draft'),('validate', 'Validate') , ('reject', 'Reject'),('done', 'Done')],default='draft')
      shift_id = fields.Many2one('resource.calendar.attendance',string='shift')
      att_date=fields.Datetime(string='Attendance date')

      def btn_ok(self):
            for rec1 in self.ids:
              rec = self.browse(rec1)
              if rec.status == 'draft':
                 rec.status = 'validate'
                 self.check_payroll(rec)
            # raise  UserError('ok' + str(self.id))

      def btn_no(self):
            for rec1 in self.ids:
              rec = self.browse(rec1)
              if rec.status == 'draft':
                 rec.status = 'reject'
                 self.check_payroll(rec)
            #raise UserError(_('no' + str(self.id)))

      def btn_ok2(self):
            for rec1 in self.ids:
              rec=self.browse(rec1)
              if rec.status2 == 'draft':
                rec.status2 = 'validate'
                self.check_payroll(rec)


      def btn_no2(self):
            for rec1 in self.ids:
              rec = self.browse(rec1)
              if rec.status2 == 'draft':
                 rec.status2 = 'reject'
                 self.check_payroll(rec)

            # raise UserError(_('no' + str(self.id)))

      def interval_to_int(self,st):
            sign=1
            res=0
            if len(st)==9:
                  sign=-1
                  res = int(st[1: 3]) * 60 + int(st[4: 6])
            else:
                  res = int(st[0: 2]) * 60 + int(st[3: 5])
            return sign*res



      def check_payroll(self,rec):
            if (rec.status in ('reject','validate')) and (rec.status2 in ('reject','validate')):

                  cod_ATTEND=self.env['hr.work.entry.type'].sudo().search([('code', '=', 'ATTEND')], limit=1).id
                  cod_LATE=self.env['hr.work.entry.type'].sudo().search([('code', '=', 'LATE')], limit=1).id
                  cod_ERLYOUT=self.env['hr.work.entry.type'].sudo().search([('code', '=', 'ERLYOUT')], limit=1).id
                  cod_BONUSENTRY=self.env['hr.work.entry.type'].sudo().search([('code', '=', 'ERLYIN')], limit=1).id
                  cod_OVT1=self.env['hr.work.entry.type'].sudo().search([('code', '=', 'OVT1')], limit=1).id
                  cod_OVT2=self.env['hr.work.entry.type'].sudo().search([('code', '=', 'OVT2')], limit=1).id

                  min_in=self.interval_to_int(rec.diff_entry)
                  min_out= self.interval_to_int(rec.diff_Exit)
                  res_entry=None
                  res_exit=None
                  late_entry=None
                  early_exit = None
                  bonus_entry = None
                  bonus_exit1 = None
                  bonus_exit2 = None
                  if rec.status=='reject':
                        if min_in<0:
                            res_entry=rec.date_in+timedelta(minutes=min_in)
                        else:
                            res_entry = rec.date_in +timedelta(minutes=-1*min_in)
                  elif rec.status=='validate':
                        if min_in<0:
                             if -1*min_in>rec.employee_id.resource_calendar_id.late_enter:
                                   res_entry = rec.date_in
                                   late_entry=rec.date_in + timedelta(minutes=min_in)
                             else:
                                   res_entry = rec.date_in + timedelta(minutes=min_in)
                        else:
                              res_entry = rec.date_in + timedelta(minutes=min_in)
                              if min_in>rec.employee_id.resource_calendar_id.early_overtime:
                                   bonus_entry =rec.date_in



                  if rec.status2=='reject':
                        if min_out<0:
                            res_exit=rec.date_out+timedelta(minutes=-1*min_out)
                        else:
                            res_exit = rec.date_out - timedelta(minutes=min_out)
                  elif rec.status2=='validate':
                        if min_out<0:
                             if -1*min_out>rec.employee_id.resource_calendar_id.early_exit:
                                   res_exit = rec.date_out
                                   early_exit=rec.date_out + timedelta(minutes=-1*min_out)
                             else:
                                   res_exit=rec.date_out+timedelta(minutes=-1*min_out)
                        else:
                              ovt1=rec.employee_id.resource_calendar_id.overtime1
                              ovt2=rec.employee_id.resource_calendar_id.overtime2
                              res_exit = rec.date_out - timedelta(minutes=min_out)
                              if min_out>ovt1:
                                   bonus_exit1 =rec.date_out
                                   if ovt2>ovt1 and min_out>ovt2:
                                       bonus_exit2 = rec.date_out
                                       bonus_exit1 = rec.date_out-timedelta(minutes=ovt2-ovt1)

                  qry = f"""
                  insert into hr_work_entry
                  (name,employee_id,work_entry_type_id,date_start,date_stop,company_id,contract_id,state,active,duration)
                  select 'attendance{rec.id}' ,employee_id,{cod_ATTEND},'{res_entry}'
                  ,'{res_exit}',hr_employee.company_id,hr_employee.contract_id,'draft',true,
                  EXTRACT(EPOCH FROM (timestamp '{res_exit}'-timestamp '{res_entry}'))/3600
                  from od_attpayroll inner join hr_employee on 
                  hr_employee.id=od_attpayroll.employee_id
                  where od_attpayroll.id={rec.id}
                  """
                  self._cr.execute(qry)
                  qry=f"""delete from hr_work_entry where work_entry_type_id=1 and employee_id={rec.employee_id.id} and
                  ((date_start<timestamp '{res_entry}' and date_stop>timestamp '{res_entry}') or
                  (date_start<timestamp '{res_exit}' and date_stop>timestamp '{res_exit}')  or
                  (date_start>=timestamp '{res_entry}' and date_stop<=timestamp '{res_exit}') )
                  
"""
                  self._cr.execute(qry)
                  if late_entry:
                        qry = f"""
                              insert into hr_work_entry
                              (name,employee_id,work_entry_type_id,date_start,date_stop,company_id,contract_id,state,active,duration)
                              select 'late enter{rec.id}' ,employee_id,{cod_LATE},'{late_entry}'
                              ,'{res_entry}',hr_employee.company_id,hr_employee.contract_id,'draft',true,
                              EXTRACT(EPOCH FROM (timestamp '{res_entry}'-timestamp '{late_entry}'))/3600
                              from od_attpayroll inner join hr_employee on 
                              hr_employee.id=od_attpayroll.employee_id
                              where od_attpayroll.id={rec.id}
                              """
                        self._cr.execute(qry)
                        qry = f"""delete from hr_work_entry where work_entry_type_id=1 and employee_id={rec.employee_id.id} and
                              date_start<timestamp '{late_entry}' and date_stop>timestamp '{late_entry}'
                        """
                        self._cr.execute(qry)
                  if early_exit:
                        qry = f"""
                              insert into hr_work_entry
                              (name,employee_id,work_entry_type_id,date_start,date_stop,company_id,contract_id,state,active,duration)
                              select 'early exit{rec.id}' ,employee_id,{cod_ERLYOUT},'{res_exit}'
                              ,'{early_exit}',hr_employee.company_id,hr_employee.contract_id,'draft',true,
                              EXTRACT(EPOCH FROM (timestamp '{early_exit}'-timestamp '{res_exit}'))/3600
                              from od_attpayroll inner join hr_employee on 
                              hr_employee.id=od_attpayroll.employee_id
                              where od_attpayroll.id={rec.id}
                              """
                        self._cr.execute(qry)
                        qry = f"""delete from hr_work_entry where work_entry_type_id=1 and employee_id={rec.employee_id.id} and
                              date_start<timestamp '{early_exit}' and date_stop>timestamp '{early_exit}'
                              """
                        self._cr.execute(qry)
                  if bonus_entry:
                        qry = f"""
                              insert into hr_work_entry
                              (name,employee_id,work_entry_type_id,date_start,date_stop,company_id,contract_id,state,active,duration)
                              select 'bonus early {rec.id}' ,employee_id,{cod_BONUSENTRY},'{bonus_entry}'
                              ,'{res_entry}',hr_employee.company_id,hr_employee.contract_id,'draft',true,
                              EXTRACT(EPOCH FROM (timestamp '{res_entry}'-timestamp '{bonus_entry}'))/3600
                              from od_attpayroll inner join hr_employee on 
                              hr_employee.id=od_attpayroll.employee_id
                              where od_attpayroll.id={rec.id}
                              """
                        self._cr.execute(qry)
                        qry = f"""delete from hr_work_entry where work_entry_type_id=1 and employee_id={rec.employee_id.id} and
                              date_start<timestamp '{bonus_entry}' and date_stop>timestamp '{bonus_entry}'
                              """
                        self._cr.execute(qry)
                  if bonus_exit1:
                        qry = f"""
                              insert into hr_work_entry
                              (name,employee_id,work_entry_type_id,date_start,date_stop,company_id,contract_id,state,active,duration)
                              select 'overtime1 {rec.id}' ,employee_id,{cod_OVT1},'{res_exit}'
                              ,'{bonus_exit1}',hr_employee.company_id,hr_employee.contract_id,'draft',true,
                              EXTRACT(EPOCH FROM (timestamp '{bonus_exit1}'-timestamp '{res_exit}'))/3600
                              from od_attpayroll inner join hr_employee on 
                              hr_employee.id=od_attpayroll.employee_id
                              where od_attpayroll.id={rec.id}
                              """
                        self._cr.execute(qry)
                        qry = f"""delete from hr_work_entry where work_entry_type_id=1 and employee_id={rec.employee_id.id} and
                              date_start<timestamp '{bonus_exit1}' and date_stop>timestamp '{bonus_exit1}'
                              """
                        self._cr.execute(qry)
                  if bonus_exit2:
                        qry = f"""
                              insert into hr_work_entry
                              (name,employee_id,work_entry_type_id,date_start,date_stop,company_id,contract_id,state,active,duration)
                              select 'overtime2 {rec.id}' ,employee_id,{cod_OVT2},'{bonus_exit1}'
                              ,'{bonus_exit2}',hr_employee.company_id,hr_employee.contract_id,'draft',true,
                              EXTRACT(EPOCH FROM (timestamp '{bonus_exit2}'-timestamp '{bonus_exit1}'))/3600
                              from od_attpayroll inner join hr_employee on 
                              hr_employee.id=od_attpayroll.employee_id
                              where od_attpayroll.id={rec.id}
                              """
                        self._cr.execute(qry)
                        qry = f"""delete from hr_work_entry where work_entry_type_id=1 and employee_id={rec.employee_id.id} and
                              date_start<timestamp '{bonus_exit2}' and date_stop>timestamp '{bonus_exit2}'
                              """
                        self._cr.execute(qry)
                  rec.status='done'
                  rec.status2='done'





      def action_transfer(self):
            if self.tranfer_payroll():
                  notification = {
                        'type': 'ir.actions.client',
                        'tag': 'display_notification',
                        'params': {
                              'title': ('Finger prints'),
                              'message': 'Transfer to payroll is completed successfully',
                              'type': 'success',  # types: success,warning,danger,info
                              'sticky': False,  # True/False will display for few seconds if false
                        },
                  }
                  return notification

      def tranfer_payroll(self):
            n_cr=self._cr
            diff_hour = -3
            odoobot = self.env['res.users'].browse(1)
            tt = datetime.now(pytz.timezone(odoobot.env.user.tz)).strftime('%z')
            diff_hour = int(tt[1:3]) + int(tt[3:]) / 60
            if tt[0:1] == '+':
                  diff_hour = -1 * diff_hour
            qry=f"""
            insert into od_attpayroll (employee_id,"inout",date_in,diff_entry,date_out,"diff_Exit",status,shift_id,att_date,status2)
select EE.id,AA.id,AA.date_in,
(AA.att_date-AA.date_in)+interval '1 hours'*(rca.hour_from+{diff_hour}) as diffin,AA.date_out,
AA.date_out-(AA.att_date+interval '1 hours'*
			(rca.hour_from+{diff_hour}+
(case when COALESCE(rca.duration,0)=0 then rca.hour_to-rca.hour_from else rca.duration end))) as diffout
,'draft',AA.shift_id,AA.att_date,'draft'
            from od_inout AS AA left join od_attpayroll AS B on AA.id=B.inout
            inner join hr_employee AS EE on EE.studio_employee_number=AA.emp_deviceno
            inner join resource_calendar_attendance
			 as  rca on rca.id= AA.shift_id
            where B.id is null
            """
            print(qry)
            n_cr.execute(qry)
            return True
