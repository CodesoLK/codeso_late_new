# -*- coding: utf-8 -*-
from flectra import fields, api, models, _
from datetime import date,datetime,timedelta
from ast import literal_eval
import datetime
import time
from flectra.tools import DEFAULT_SERVER_DATETIME_FORMAT
from dateutil.relativedelta import relativedelta
import pytz
from zk import ZK, const
import socket


class Attendence_Download(models.TransientModel):
    _name = 'attendence.download'
    _description = 'Attendence Download Wizard'

    attendence_date = fields.Date(string="Attendence Date")

    def man_download_attendence_wizard(self):
        date_to_filter1 = self.attendence_date
        date_to_filter =date_to_filter1+" 00:00:00"
        print("Here.........: ",date_to_filter)
        ip_addres = socket.gethostbyname('v-smart-trading-asia.dyndns.biz')
        # socket.gethostbyname('www.google.com')
        # print(ip_addres)
        conn = None
        zk = ZK(ip_addres, port=4370, timeout=40, ommit_ping=False)
        try:
            #print ('Connecting to device ...')
            conn = zk.connect()
            conn.disable_device()
            #print ('Firmware Version: : {}'.format(conn.get_firmware_version()))
            attendances = conn.get_attendance()
            # for x in attendances:
            #     print(x)
            #print(attendances)
            users_get = conn.get_users()
            user = [[x.user_id,x.name]for x in users_get]
            zk_attendance = self.env['zk.machine.attendance']
            att_obj = self.env['hr.attendance']
            #list1 = [ "2", "2020-10-06 18:20:41", (1, 255)]
            device_attendance = [[x.user_id, x.timestamp, x.punch] for x in attendances]
            if device_attendance:
                for each in device_attendance:
                    #print (each)
                    atten_time = each[1]
                    start_date = atten_time  
                    con_set_date = datetime.datetime(start_date.year, start_date.month, start_date.day)
                    atten_time = datetime.datetime.strptime(atten_time.strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
                    local_tz = pytz.timezone(self.env.user.partner_id.tz or 'GMT')
                    local_dt = local_tz.localize(atten_time, is_dst=None)
                    utc_dt = local_dt.astimezone(pytz.utc)
                    utc_dt = utc_dt.strftime("%Y-%m-%d %H:%M:%S")
                    atten_time = datetime.datetime.strptime(utc_dt, "%Y-%m-%d %H:%M:%S")-timedelta(hours=5,minutes=30)
                    atten_time_test = con_set_date
                    if (str(date_to_filter)) != (str(atten_time_test)):
                        continue
                    else:
                        #print("........................>>>>>",atten_time_test,"=====",date_to_filter)
                        pass
                    atten_time = fields.Datetime.to_string(atten_time)
                    
                    if user:
                            for uid in user:
                                if str(uid[0]) == str(each[0]):
                                    print("true uid",uid[0])
                                    get_user_id = self.env['hr.employee'].search(
                                        [('device_id', '=', str(each[0]))])
                                    if get_user_id:
                                        duplicate_atten_ids = att_obj.search(
                                            [('employee_id', '=', get_user_id.id), ('check_in', '=', atten_time)])
                                        duplicate_atten_ids_out = att_obj.search(
                                            [('employee_id', '=', get_user_id.id), ('check_out', '=', atten_time)])
                                        if duplicate_atten_ids:
                                            continue
                                        elif duplicate_atten_ids_out:
                                            continue
                                        else:
                                            #print("point 1 .............................................")
                                            zk_attendance.create({'employee_id': get_user_id.id,
                                                                  'device_id': each[0],
                                                                  'attendance_type': str(15),
                                                                  'punch_type': str(2),
                                                                  'punching_time': atten_time,
                                                                  })
                                            att_var = att_obj.search([('employee_id', '=', get_user_id.id),
                                                                      ('check_out', '=', False)])
                                            if each[2] == 0 or 255: #check-in
                                                if not att_var:
                                                    att_obj.create({'employee_id': get_user_id.id,
                                                                    'check_in': atten_time})
                                                elif att_var:
                                                    if len(att_var) == 1:
                                                        #att_var2=att_obj.search([('employee_id', '=', get_user_id.id)])
                                                        att_var.write({'check_out': atten_time})
                                                    else:
                                                        att_var1 = att_obj.search([('employee_id', '=', get_user_id.id)])
                                                        if att_var1:
                                                            att_var1[-1].write({'check_out': atten_time})

                                            #if each[3] == 1: #check-out
                                            #    if not att_var:
                                            #        att_obj.create({'employee_id': get_user_id.id,
                                            #                        'check_in': atten_time})
                                            #    elif att_var:
                                            #        if len(att_var) == 1:
                                            #            att_var2=att_obj.search([('employee_id', '=', get_user_id.id)])
                                            #            att_var2[-1].write({'check_out': atten_time})
                                            #        else:
                                            #            att_var1 = att_obj.search([('employee_id', '=', get_user_id.id)])
                                            #            if att_var1:
                                            #                att_var1[-1].write({'check_out': atten_time})

                                    else:
                                        #print("point 2 .............................................")
                                        employee = self.env['hr.employee'].create(
                                            {'device_id': str(each[0]), 'name': (uid[1])})
                                        zk_attendance.create({'employee_id': employee.id,
                                                              'device_id': each[0],
                                                              'attendance_type': str(15),
                                                              'punch_type': str(2),
                                                              'punching_time': atten_time,
                                                              })
                                        att_obj.create({'employee_id': employee.id,
                                                        'check_in': atten_time})
                                else:
                                    pass
                else:
                    print("eroror")                    
        finally:
            if conn:
                conn.disconnect()
    def man_download_attendence_wizard_all(self):
        # date_to_filter1 = self.attendence_date
        # date_to_filter =date_to_filter1+" 00:00:00"
        # print("Here.........: ",date_to_filter)
        ip_addres = socket.gethostbyname('v-smart-trading-asia.dyndns.biz')
        # socket.gethostbyname('www.google.com')
        # print(ip_addres)
        conn = None
        zk = ZK(ip_addres, port=4370, timeout=40, ommit_ping=False)
        try:
            #print ('Connecting to device ...')
            conn = zk.connect()
            conn.disable_device()
            #print ('Firmware Version: : {}'.format(conn.get_firmware_version()))
            attendances = conn.get_attendance()
            # for x in attendances:
            #     print(x)
            #print(attendances)
            users_get = conn.get_users()
            user = [[x.user_id,x.name]for x in users_get]
            zk_attendance = self.env['zk.machine.attendance']
            att_obj = self.env['hr.attendance']
            #list1 = [ "2", "2020-10-06 18:20:41", (1, 255)]
            device_attendance = [[x.user_id, x.timestamp, x.punch] for x in attendances]
            if device_attendance:
                for each in device_attendance:
                    #print (each)
                    atten_time = each[1]
                    start_date = atten_time  
                    #con_set_date = datetime.datetime(start_date.year, start_date.month, start_date.day)
                    atten_time = datetime.datetime.strptime(atten_time.strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
                    local_tz = pytz.timezone(self.env.user.partner_id.tz or 'GMT')
                    local_dt = local_tz.localize(atten_time, is_dst=None)
                    utc_dt = local_dt.astimezone(pytz.utc)
                    utc_dt = utc_dt.strftime("%Y-%m-%d %H:%M:%S")
                    atten_time = datetime.datetime.strptime(utc_dt, "%Y-%m-%d %H:%M:%S")-timedelta(hours=5,minutes=30)
                    #atten_time_test = con_set_date
                    # if (str(date_to_filter)) != (str(atten_time_test)):
                    #     continue
                    # else:
                    #     print("........................>>>>>",atten_time_test,"=====",date_to_filter)
                    atten_time = fields.Datetime.to_string(atten_time)
                    
                    if user:
                            for uid in user:
                                if str(uid[0]) == str(each[0]):
                                    #print("true uid",uid[0])
                                    get_user_id = self.env['hr.employee'].search(
                                        [('device_id', '=', str(each[0]))])
                                    if get_user_id:
                                        duplicate_atten_ids = att_obj.search(
                                            [('employee_id', '=', get_user_id.id), ('check_in', '=', atten_time)])
                                        duplicate_atten_ids_out = att_obj.search(
                                            [('employee_id', '=', get_user_id.id), ('check_out', '=', atten_time)])
                                        if duplicate_atten_ids:
                                            continue
                                        elif duplicate_atten_ids_out:
                                            continue
                                        else:
                                            #print("point 1 .............................................")
                                            zk_attendance.create({'employee_id': get_user_id.id,
                                                                  'device_id': each[0],
                                                                  'attendance_type': str(15),
                                                                  'punch_type': str(2),
                                                                  'punching_time': atten_time,
                                                                  })
                                            att_var = att_obj.search([('employee_id', '=', get_user_id.id),
                                                                      ('check_out', '=', False)])
                                            if each[2] == 0 or 255: #check-in
                                                if not att_var:
                                                    att_obj.create({'employee_id': get_user_id.id,
                                                                    'check_in': atten_time})
                                                elif att_var:
                                                    if len(att_var) == 1:
                                                        #att_var2=att_obj.search([('employee_id', '=', get_user_id.id)])
                                                        att_var.write({'check_out': atten_time})
                                                    else:
                                                        att_var1 = att_obj.search([('employee_id', '=', get_user_id.id)])
                                                        if att_var1:
                                                            att_var1[-1].write({'check_out': atten_time})

                                            #if each[3] == 1: #check-out
                                            #    if not att_var:
                                            #        att_obj.create({'employee_id': get_user_id.id,
                                            #                        'check_in': atten_time})
                                            #    elif att_var:
                                            #        if len(att_var) == 1:
                                            #            att_var2=att_obj.search([('employee_id', '=', get_user_id.id)])
                                            #            att_var2[-1].write({'check_out': atten_time})
                                            #        else:
                                            #            att_var1 = att_obj.search([('employee_id', '=', get_user_id.id)])
                                            #            if att_var1:
                                            #                att_var1[-1].write({'check_out': atten_time})

                                    else:
                                        #print("point 2 .............................................")
                                        employee = self.env['hr.employee'].create(
                                            {'device_id': str(each[0]), 'name': (uid[1])})
                                        zk_attendance.create({'employee_id': employee.id,
                                                              'device_id': each[0],
                                                              'attendance_type': str(15),
                                                              'punch_type': str(2),
                                                              'punching_time': atten_time,
                                                              })
                                        att_obj.create({'employee_id': employee.id,
                                                        'check_in': atten_time})
                                else:
                                    pass
                else:
                    print("eroror")                    
        finally:
            if conn:
                conn.disconnect()

