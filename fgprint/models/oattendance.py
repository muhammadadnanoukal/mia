import time

import odoo.exceptions
from odoo import models, fields
from .zkd import ZK
#from .suprema import download as downloadsup2
from datetime import datetime, timedelta
import pytz


class Attendance(models.Model):
    _name = 'od.attendance'
    _description = 'Attendance Record'

    log_seq = fields.Integer(string='Sequence', index=True)
    log_userid = fields.Integer(string='User', index=True)
    log_date = fields.Datetime(string='Date/time', index=True)
    log_device = fields.Many2one('od.device', 'device', index=True)

    def action_process(self):
        rec_settings=self.env['od.fp.settings'].sudo().search([('setting_name', '=', 'Source mode')], limit=1)
        if rec_settings[0].setting_value==1:
            rec_settings_lastid = self.env['od.fp.settings'].sudo().search([('setting_name', '=', 'Attendance Seq')], limit=1)
            last_att_id=rec_settings_lastid[0].setting_value
            # print('entered handling')
            new_cr = self._cr
            query = f"""insert into od_inout (emp_deviceno,date_in,date_out,date_inflag,date_outflag)
                     select B.studio_employee_number, date_trunc('minute',A.check_in),date_trunc('minute',A.check_out),'internal','internal' 
                     from hr_attendance as A inner join hr_employee as B on A.employee_id=B.id
                     where A.id>='{last_att_id}'
            """
            new_cr.execute(query)
            new_cr.execute("update od_fp_settings set setting_value=(select max(id) from hr_attendance) where setting_name='Attendance Seq'")

            print(last_att_id)
            notification = {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': ('Finger prints'),
                    'message': 'Attendance fetching is completed successfully',
                    'type': 'success',  # types: success,warning,danger,info
                    'sticky': False,  # True/False will display for few seconds if false
                },
            }
            return notification
        elif self.handle_all_cases():
            notification = {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': ('Finger prints'),
                    'message': 'Attendance Process is completed successfully',
                    'type': 'success',  # types: success,warning,danger,info
                    'sticky': False,  # True/False will display for few seconds if false
                },
            }
            return notification

    def action_transfer(self):
        rec_settings=self.env['od.fp.settings'].sudo().search([('setting_name', '=', 'Source mode')], limit=1)
        if rec_settings[0].setting_value==1:
            notification = {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': ('Finger prints'),
                    'message': 'No action is done for a given mode',
                    'type': 'info',  # types: success,warning,danger,info
                    'sticky': False,  # True/False will display for few seconds if false
                },
            }
            return notification
        elif self.handledata_attendance():
            notification = {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': ('Finger prints'),
                    'message': 'Attendance Transfer is completed successfully',
                    'type': 'success',  # types: success,warning,danger,info
                    'sticky': False,  # True/False will display for few seconds if false
                },
            }
            return notification

    # download data and fill the log table using longthread function
    def action_start(self):

        if self.longthread():
            notification = {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': ('Finger prints'),
                    'message': 'Download is done',
                    'type': 'success',  # types: success,warning,danger,info
                    'sticky': False,  # True/False will display for few seconds if false
                },
            }
            return notification
        else:
            notification = {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': ('Finger prints'),
                    'message': 'Download in failed',
                    'type': 'warning',  # types: success,warning,danger,info
                    'sticky': False,  # True/False will display for few seconds if false
                },
            }
            return notification

    def longthread(self):
        try:
            # print('entered....................')

            # atts = []
            res = self.env['od.device'].search([])
            for dd in res:
                if (dd.device_enables):
                    atts_t = None
                    if dd.device_model == 'zk':
                        atts_t = self.downloadzk(dd.device_name, dd.device_port)
                        if atts_t:
                            self._cr.autocommit(False)
                            if dd.last_seq:
                                lastseq = dd.last_seq
                            else:
                                lastseq = 0
                            nseq = 0
                            seqdate = None
                            for eachrec in atts_t:
                                nseq += 1
                                seqdate = eachrec.timestamp
                                #  if seqdate >= datetime(year=seqdate.year, month=3, day=29) and seqdate <= datetime(year=seqdate.year, month=10, day=28):
                                #    seqdate+=timedelta(hours=-1)
                                if nseq > lastseq:
                                    super(Attendance, self).create({'log_seq': nseq,
                                                                    'log_userid': eachrec.user_id,
                                                                    'log_date': seqdate,
                                                                    'log_device': dd.id})
                                    # atts.append(eachrec)
                            dd.update({'last_seq': nseq, 'download_date': seqdate})
                            self._cr.commit()
                    elif dd.device_model == 'suprema':
                        lastseq = 0
                        if dd.last_seq:
                            lastseq = dd.last_seq

                        print('show me')
                        atts_t = self.downloadsuprema(dd.device_name, dd.device_port,lastseq)
                        if atts_t:
                            self._cr.autocommit(False)
                            for eachrec in atts_t:
                                seqdate = eachrec['timestamp']
                                nseq=eachrec['ID']
                                super(Attendance, self).create({'log_seq': nseq,
                                                                    'log_userid': eachrec['userID'],
                                                                    'log_date': seqdate,
                                                                    'log_device': dd.id})

                            dd.update({'last_seq': nseq, 'download_date': seqdate})
                            self._cr.commit()



            return True
        except Exception as ex:
            # print('error 1')
            self._cr.rollback()
            self._cr.autocommit(True)
            self.env['fp.logerror'].create(
                {'log_date': datetime.now(), 'log_device': dd.id, 'device_error': format(ex)})

            # raise Warning()
            return False

    # def handleinout(self,atts):
    #     attsort = sorted(atts, key=lambda x: (x.user_id, x.timestamp))
    #     for eachirec in attsort:
    #         att_emp=self.env['hr.employee'].search([('studio_employee_number','=',eachirec.user_id)], limit=1)
    #         if att_emp:
    #             inoutatt=self.env['hr.attendance'].search(
    #             [('employee_id', '=', att_emp[0].id), ('check_out', '=', False), ('check_in', '!=', False)],
    #             limit=1)
    #             if inoutatt:
    #                 inoutatt[0].update({'check_out': eachirec.timestamp})
    #             else:
    #                 self.env['hr.attendance'].create({'employee_id': att_emp[0].id, 'check_in': eachirec.timestamp })
    #
    #         inoutrec = self.env['od.inout'].search(
    #             [('emp_deviceno', '=', eachirec.user_id), ('date_out', '=', False), ('date_in', '!=', False)],
    #             limit=1)
    #         if inoutrec:
    #             inoutrec[0].update({'date_out': eachirec.timestamp})
    #         else:
    #             self.env['od.inout'].create({'emp_deviceno': eachirec.user_id, 'date_in': eachirec.timestamp})
    #

    def handledata_attendance(self):
        new_cr = self.pool.cursor()
        new_cr = self._cr
        query = """ select od_inout.*,hr_attendance.id as id_attend from 
          od_inout inner join hr_attendance on od_inout.id=hr_attendance.inout_ref
          where od_inout.date_out is not null and hr_attendance.check_out is null
          """
        new_cr.execute(query)
        values = new_cr.dictfetchall()
        last_id = 0
        if len(values) > 0:
            for index in range(0, len(values)):
                rec = self.env['hr.attendance'].browse(values[index].get('id_attend'))
                rec[0].update({'check_out': values[index].get('date_out')})

        last_attenance_rec = 0
        rec_settings = self.env['od.fp.settings'].sudo().search([('setting_name', '=', 'last_attendance')], limit=1)

        if rec_settings:
            last_attenance_rec = rec_settings[0].setting_value

        query = """select od_inout.*,hr_employee.id as employee_id from od_inout 
          inner join hr_employee on  od_inout.emp_deviceno=hr_employee.studio_employee_number 
          where od_inout.id> 
          """ + str(last_attenance_rec) + " order by od_inout.id"
        new_cr.execute(query)
        values = new_cr.dictfetchall()
        last_id = 0
        if len(values) > 0:
            for index in range(0, len(values)):
                last_id = values[index].get('id')
                self.env['hr.attendance'].create(
                    {'employee_id': values[index].get('employee_id'), 'check_in': values[index].get('date_in'),
                     'check_out': values[index].get('date_out'), 'inout_ref': values[index].get('id')})
                # if not new_cr.rowcount:
                #     new_cr.execute(
                #     f"insert into hr_attendance (employee_id,check_in,x_studio_shift_id) values ({values[index].get('employee_id')},TIMESTAMP '{values[index].get('log_date')}','{values[index].get('resource_calendar_id')}') ")
                if (last_id % 250 == 0):
                    new_cr.execute(
                        f"update od_fp_settings set setting_value={last_id} where setting_name='last_attendance'")
                    if not new_cr.rowcount:
                        new_cr.execute(
                            f"insert into od_fp_settings (setting_name,setting_value) values ('last_attendance',{last_id}) ")
                    new_cr.commit()
            new_cr.execute(f"update od_fp_settings set setting_value={last_id} where setting_name='last_attendance'")
            if not new_cr.rowcount:
                new_cr.execute(
                    f"insert into od_fp_settings (setting_name,setting_value) values ('last_attendance',{last_id}) ")
            # new_cr.commit()
            # new_cr.close()

            new_cr.commit()
        return True

    # classic handle data for all users (depricated)
    def handledata(self):
        new_cr = self._cr
        query = """select od_attendance.* from od_attendance 
          inner join od_device on od_attendance.log_device = od_device.id
          where od_attendance.log_seq > od_device.treat_seq
          order by od_attendance.log_userid,od_attendance.log_date
          """
        new_cr.execute(query)

        values = new_cr.dictfetchall()
        for index in range(0, len(values)):
            new_cr.execute(
                f"update od_inout set date_out=TIMESTAMP '{values[index].get('log_date')}' where emp_deviceno={values[index].get('log_userid')} and date_in is not null and date_out is null")
            if not new_cr.rowcount:
                new_cr.execute(
                    f"insert into od_inout (emp_deviceno,date_in) values ({values[index].get('log_userid')},TIMESTAMP '{values[index].get('log_date')}') ")
        re = new_cr.execute("update od_device set treat_seq=last_seq")
        return True

    # classic handle data
    def handle_all_cases(self):
        # user_tz = self.env.user.tz

        diff_hour=-3
        #self.env['blog.post'].with_user(1).browse(1)
        odoobot = self.env['res.users'].browse(1)
        # print(odoobot.env.user.tz)
   #     print(odoobot.tz)
        tt=datetime.now(pytz.timezone(odoobot.env.user.tz)).strftime('%z')
        # print(tt)
        # print(int(tt[1:3]))
        diff_hour=int(tt[1:3])+int(tt[3:])/60
        if tt[0:1] == '+':
            diff_hour=-1*diff_hour
        # diff_hour=0
        # print(diff_hour)
        # print('------utc')
        # print(datetime.utcnow())
        # print('------now')
        # print(datetime)
        # print('------shell')
        # x=pytz.all_timezones
        # print(x)
        # print('=================================')
        #
        # print( tzlocal.get_localzone())
        # print(time.clock())
        # print(time.timezone())
        # ggg=subprocess.check_output(['date','+%Z'])
        # print(ggg)
        # print('------timezone2 ')
        # self._cr.execute("SELECT EXTRACT(TIMEZONE FROM now())/3600.0 as tz")
        # vv=self._cr.dictfetchall()
        # print(vv[0].get('tz'))
        last_date_rec = None
        rec_settings = self.env['od.fp.settings'].sudo().search([('setting_name', '=', 'last_date')], limit=1)
        if rec_settings:
            last_date_rec = self.to_date_integer(rec_settings.setting_value)

        fromdate = ''
        if not last_date_rec:
            fromdate = (datetime.now() + timedelta(days=-150)).strftime('%Y-%m-%d')
        else:
            fromdate = (last_date_rec + timedelta(days=1)).strftime('%Y-%m-%d')
        todate = datetime.now().strftime('%Y-%m-%d')

        new_cr = self._cr
        self.handledata_sequential()
        self.handledata_daily(diff_hour)

        new_cr.execute(f""" delete from od_inout where date_in >='{fromdate}' and 
          emp_deviceno in (select studio_employee_number from hr_employee 
          where hr_employee.att_mode in ('shift','standard','classic') )
          """)
        self.handledata_classic(diff_hour, fromdate)
        self.handledata_standard(fromdate, todate,diff_hour)
        self.handledata_shift(fromdate, todate,diff_hour)
        new_cr.execute("update od_device set treat_seq=last_seq")
        qry = f"update od_fp_settings set setting_value={self.to_integer(todate)} where setting_name='last_date'"
        # print(qry)
        new_cr.execute(qry)
        if not new_cr.rowcount:
            new_cr.execute(
                f"insert into od_fp_settings (setting_name,setting_value) values ('last_date',{self.to_integer(todate)}) ")
        return True

    def handledata_sequential(self):
        new_cr = self._cr
        query = """select od_attendance.* from od_attendance 
          inner join od_device on od_attendance.log_device = od_device.id
          inner join hr_employee on od_attendance.log_userid=hr_employee.studio_employee_number
          where od_attendance.log_seq > od_device.treat_seq and hr_employee.att_mode='sequential'
          order by od_attendance.log_userid,od_attendance.log_date
          """
        new_cr.execute(query)

        values = new_cr.dictfetchall()
        for index in range(0, len(values)):
            new_cr.execute(
                f"update od_inout set date_out=date_trunc('minute',TIMESTAMP '{values[index].get('log_date')}') where emp_deviceno={values[index].get('log_userid')} and date_in is not null and date_out is null")
            if not new_cr.rowcount:
                new_cr.execute(
                    f"insert into od_inout (emp_deviceno,date_in) values ({values[index].get('log_userid')},date_trunc('minute',TIMESTAMP '{values[index].get('log_date')}')) ")
        #  re = new_cr.execute("update od_device set treat_seq=last_seq")
        return True

    def handledata_daily(self,diff1):
        new_cr = self._cr
        query = """select od_attendance.* from od_attendance 
          inner join od_device on od_attendance.log_device = od_device.id
          inner join hr_employee on od_attendance.log_userid=hr_employee.studio_employee_number
          where od_attendance.log_seq > od_device.treat_seq and hr_employee.att_mode='daily'
          order by od_attendance.log_userid,od_attendance.log_date
          """
        # print(query)
        new_cr.execute(query)

        values = new_cr.dictfetchall()
        last_emp = None
        last_date = None
        just_in = False
        for index in range(0, len(values)):
            # print(type(values[index].get('log_date')))
            # print('-----')
            # print(values[index].get('log_date'))
            if just_in and (
                    last_emp != values[index].get('log_userid') or last_date != values[index].get('log_date').date()):
                out_time = self.get_emp_last_exit(last_emp, last_date,diff1)
                qqq = f"update od_inout set date_out=TIMESTAMP '{out_time}',date_outflag='setting' where emp_deviceno={last_emp} and date(date_in)='{last_date}' and date_out is null"
                # print(qqq)
                new_cr.execute(qqq)

            last_emp = values[index].get('log_userid')
            last_date = values[index].get('log_date').date()
            strq = f"update od_inout set date_out=date_trunc('minute',TIMESTAMP '{values[index].get('log_date')}') where emp_deviceno={values[index].get('log_userid')} and date(date_in)='{(values[index].get('log_date')).date()}' and date_out is null"
            # print('q is -----')
            # print(strq)
            new_cr.execute(strq)
            just_in = False
            if not new_cr.rowcount:
                just_in = True
                new_cr.execute(
                    f"insert into od_inout (emp_deviceno,date_in) values ({values[index].get('log_userid')},date_trunc('minute',TIMESTAMP '{values[index].get('log_date')}')) ")
        #  re = new_cr.execute("update od_device set treat_seq=last_seq")
        if just_in:
            out_time = self.get_emp_last_exit(last_emp, last_date,diff1)
            qqq = f"update od_inout set date_out=TIMESTAMP '{out_time}',date_outflag='setting' where emp_deviceno={last_emp} and date(date_in)='{last_date}' and date_out is null"
            new_cr.execute(qqq)

        return True

    def handledata_classic(self,diff1,fromdate):
        new_cr = self._cr
        query=f"""insert into od_inout (emp_deviceno,date_in,date_out,date_inflag,date_outflag)
         select log_userid, min(date_trunc('minute',log_date)),max(date_trunc('minute',log_date)),'internal','internal' from od_attendance
         inner join hr_employee on od_attendance.log_userid=hr_employee.studio_employee_number
         where  hr_employee.att_mode='classic' and log_date>='{fromdate}'
         group by log_userid, date_trunc('day',log_date)
         having count(*)>1
"""
        # print(query)
        new_cr.execute(query)

        query2=f"""          
         select log_userid, min(log_date) as ldate,date_trunc('day',log_date) as dt from od_attendance
         inner join hr_employee on od_attendance.log_userid=hr_employee.studio_employee_number
         where hr_employee.att_mode='classic' and log_date>='{fromdate}'
         group by log_userid, date_trunc('day',log_date)
         having count(*)=1"""
        new_cr.execute(query2)
        values = new_cr.dictfetchall()
        for index in range(0, len(values)):
            firstentry=self.get_emp_first_entry(values[index].get('log_userid'),values[index].get('dt'),diff1)
            lastexit=self.get_emp_last_exit(values[index].get('log_userid'),values[index].get('dt'),diff1)
            if abs(firstentry-values[index].get('ldate'))<=abs(lastexit-values[index].get('ldate')):
                qq=f"""
                insert into od_inout (emp_deviceno,date_in,date_out,date_inflag,date_outflag)
                values ({values[index].get('log_userid')},'{values[index].get('ldate')}','{lastexit}','internal','setting')"""
                new_cr.execute(qq)
            else:
                qq=f"""
                insert into od_inout (emp_deviceno,date_in,date_out,date_inflag,date_outflag)
                values ({values[index].get('log_userid')},'{firstentry}','{values[index].get('ldate')}','setting','internal')"""
                new_cr.execute(qq)



    def handledata_standard(self, fromdate, todate,diff1):
        new_cr = self._cr
        query = f"""insert into od_inout (emp_deviceno,date_in,date_out,shift_id,date_inflag,date_outflag)
          SELECT hr_employee.studio_employee_number
   ,dateIinterval.dt+
  interval '1 hours'*(resource_calendar_attendance.hour_from+{diff1})   as entry,
  case when COALESCE(resource_calendar_attendance.duration,0) =0 then
  dateIinterval.dt+
  interval '1 hours'*(resource_calendar_attendance.hour_to+{diff1} )
  else 
  dateIinterval.dt+
  interval '1 hours'*(resource_calendar_attendance.hour_from+resource_calendar_attendance.duration+{diff1} ) 
  end
  as exit,resource_calendar_attendance.id,'setting','setting'
	FROM hr_employee inner join resource_calendar_attendance
	on resource_calendar_attendance.calendar_id=hr_employee.resource_calendar_id
	inner join 
	(select extract(isodow from period.dt) - 1 as dayofweek,dt from (SELECT  generate_series('{fromdate}'::timestamp,
                              '{todate}', '1 days') as dt) as period) as dateIinterval
	on cast(resource_calendar_attendance.dayofweek as integer)=dateIinterval.dayofweek	
	where hr_employee.att_mode='standard'
           """
        new_cr.execute(query)
        return True

    def handledata_shift(self, fromdate, todate,diff_h):
        new_cr = self._cr
        # print('------------')
        # print(diff_h)
        auto = self.get_setting('AUTO_SHIFT')
        if not (auto == 1 or auto == 0):
            self.save_setting('AUTO_SHIFT', 0)
        datin_out = "fres.datin,fres.datout"
        datflg = "'internal','internal'"
        if auto == 1:
            datin_out = f"COALESCE(fres.datin,fres.chkin+interval '-1 hours'*{diff_h}),COALESCE(fres.datout,fres.chkout+interval '-1 hours'*{diff_h})"
            datflg = "case when fres.datin is null then 'setting' else 'internal' end,case when fres.datout is null then 'setting' else 'internal' end"


        query = f"""
insert into od_inout (emp_deviceno,date_in,date_out,shift_id,date_inflag,date_outflag,att_date)
select fres.studio_employee_number,{datin_out},fres.id,{datflg},fres.dt from ( 
select res.studio_employee_number,min(case when res.check = 0 then res.check_date end) as datin,max(case when res.check = 1 then res.check_date end) as datout,res.id,min(res.point) as chkin,max(res.point) as chkout,res.dt from
(
select t.dt, t.studio_employee_number,t.id,(t.point+interval '1 hours'*{diff_h}) as point,t.check,
case  when t.check=0 then min(date_trunc('minute',od_attendance.log_date)) else max(date_trunc('minute',od_attendance.log_date)) end as check_date
from
(
SELECT dateIinterval.dt,
	case when COALESCE(resource_calendar_attendance.duration,0)=0 then resource_calendar_attendance.hour_to-resource_calendar_attendance.hour_from
	 else resource_calendar_attendance.duration end as dur
   ,dateIinterval.dt+
  interval '1 hours'*(resource_calendar_attendance.hour_from +{diff_h})  as point,
  0 as check,
    resource_calendar_attendance.id,hr_employee.studio_employee_number,resource_calendar_attendance.tol_in_early as delay_early,resource_calendar_attendance.tol_in_late as delay_late
	FROM hr_employee inner join resource_calendar_attendance
	on resource_calendar_attendance.calendar_id=hr_employee.resource_calendar_id
	inner join 
	(select extract(isodow from period.dt) - 1 as dayofweek,dt from (SELECT  generate_series('{fromdate}'::timestamp,
                              '{todate}', '1 days') as dt) as period) as dateIinterval
	on cast(resource_calendar_attendance.dayofweek as integer)=dateIinterval.dayofweek	
	where hr_employee.att_mode='shift'
union
SELECT dateIinterval.dt
  ,case when COALESCE(resource_calendar_attendance.duration,0)=0 then resource_calendar_attendance.hour_to-resource_calendar_attendance.hour_from else resource_calendar_attendance.duration end as dur
  ,case when COALESCE(resource_calendar_attendance.duration,0) =0 then
  dateIinterval.dt+
  interval '1 hours'*(resource_calendar_attendance.hour_to +{diff_h}) 
  else 
  dateIinterval.dt+
  interval '1 hours'*(resource_calendar_attendance.hour_from+resource_calendar_attendance.duration) 
  end
  as point,
  1 as check, 
    resource_calendar_attendance.id,hr_employee.studio_employee_number
    ,resource_calendar_attendance.tol_out_early as delay_early,resource_calendar_attendance.tol_out_over as delay_late
	FROM hr_employee inner join resource_calendar_attendance
	on resource_calendar_attendance.calendar_id=hr_employee.resource_calendar_id
	inner join 
	(select extract(isodow from period.dt) - 1 as dayofweek,dt from (SELECT  generate_series('{fromdate}'::timestamp,
                              '{todate}', '1 days') as dt) as period) as dateIinterval
	on cast(resource_calendar_attendance.dayofweek as integer)=dateIinterval.dayofweek	
	where  hr_employee.att_mode='shift'

) as t left join od_attendance
on (t.studio_employee_number =od_attendance.log_userid
	and t.point-  (interval '1 hours'*COALESCE(delay_early,0)) <=od_attendance.log_date
	and t.point+  (interval '1 hours'*COALESCE(delay_late,0)) >=od_attendance.log_date)
group by t.dt, t.studio_employee_number,t.id,t.point,t.check
) as res
group by res.dt, res.studio_employee_number,res.id
) as fres
"""
        # where fres.datin is not null or fres.datout is not null
        print(query)
        new_cr.execute(query)
        new_cr.execute("delete from od_inout where (date_in is null and date_out is null) or (date_inflag='setting' and date_outflag='setting')")

        return True

    def downloadsuprema(self, ipaddress, portnumber,lastseq):
        atts = None
        atts=downloadsup2(ipaddress, portnumber,lastseq)


    def downloadzk(self, ipaddress, portnumber):
        errocc = False
        conn = None
        expmsg = ''
        atts = []
        zk = ZK(ipaddress, port=portnumber)
        try:
            conn = zk.connect()
            conn.disable_device()
            atts = conn.get_attendance()
            #    conn.test_voice()
            print('Enabling device ...')
            conn.enable_device()
        except Exception as e:
            errocc = True
        finally:
            if errocc:
                if conn:
                    conn.disconnect()
                    raise odoo.exceptions.Warning("Failed to download from device: " + ipaddress)
                else:
                    raise odoo.exceptions.Warning("Failed to connect device: " + ipaddress)
            else:
                return atts

    def to_integer(self, dt_time):

        x = dt_time.replace('-', '')
        return int(x)

    def to_date_integer(self, int_dt):
        chdate = str(int_dt)
        return datetime(int(chdate[0:4]), int(chdate[4:6]), int(chdate[6:]))

    def get_setting(self, settingname):
        last_date_rec = None
        rec_settings = self.env['od.fp.settings'].sudo().search([('setting_name', '=', settingname)], limit=1)
        if rec_settings:
            return rec_settings.setting_value
        else:
            return None

    def save_setting(self, settingname, settingval):
        new_cr = self._cr
        qry = f"update od_fp_settings set setting_value={settingval} where setting_name='{settingname}'"
        new_cr.execute(qry)
        if not new_cr.rowcount:
            new_cr.execute(
                f"insert into  od_fp_settings (setting_name,setting_value) values ('{settingname}',{settingval})")

    def get_emp_last_exit(self, empid, daydate,diff):
        qry = f"""select max(exit)+interval '1 hours'*{diff} as lastshift from (
SELECT hr_employee.studio_employee_number
   ,dateIinterval.dt+
  interval '1 hours'*resource_calendar_attendance.hour_from   as entry,
  case when COALESCE(resource_calendar_attendance.duration,0) =0 then
  dateIinterval.dt+
  interval '1 hours'*resource_calendar_attendance.hour_to 
  else 
  dateIinterval.dt+
  interval '1 hours'*(resource_calendar_attendance.hour_from+resource_calendar_attendance.duration) 
  end
  as exit
	FROM hr_employee inner join resource_calendar_attendance
	on resource_calendar_attendance.calendar_id=hr_employee.resource_calendar_id
	inner join 
	(select extract(isodow from period.dt) - 1 as dayofweek,dt from (SELECT  generate_series('{daydate}'::timestamp,
                              '{daydate}', '1 days') as dt) as period) as dateIinterval
	on cast(resource_calendar_attendance.dayofweek as integer)=dateIinterval.dayofweek	
	where hr_employee.studio_employee_number={empid}
	) as maxexit

"""
        new_cr = self._cr
        new_cr.execute(qry)
        values = new_cr.dictfetchall()
        for index in range(0, len(values)):
            return values[index].get('lastshift')


    def get_emp_first_entry(self, empid, daydate,diff):
        qry = f"""select min(entry)+interval '1 hours'*{diff} as firstshift from (
SELECT dateIinterval.dt+interval '1 hours'*resource_calendar_attendance.hour_from   as entry
	FROM hr_employee inner join resource_calendar_attendance
	on resource_calendar_attendance.calendar_id=hr_employee.resource_calendar_id
	inner join 
	(select extract(isodow from period.dt) - 1 as dayofweek,dt from (SELECT  generate_series('{daydate}'::timestamp,
                              '{daydate}', '1 days') as dt) as period) as dateIinterval
	on cast(resource_calendar_attendance.dayofweek as integer)=dateIinterval.dayofweek	
	where hr_employee.studio_employee_number={empid}
	) as minentry
"""
        new_cr = self._cr
        new_cr.execute(qry)
        values = new_cr.dictfetchall()
        for index in range(0, len(values)):
            return values[index].get('firstshift')

