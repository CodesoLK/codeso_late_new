from flectra import fields, api, models, _
from datetime import date,datetime,timedelta
from ast import literal_eval
import time
from flectra.tools import DEFAULT_SERVER_DATETIME_FORMAT
from dateutil.relativedelta import relativedelta

class codesoHrLate(models.Model):   
    _name = "codeso.hr.late"
    _description = "codeso Hr Late" 
    _rec_name = 'employee_id'
    _order = 'id desc'
    
    employee_id = fields.Many2one('hr.employee', string="Employee")
    manager_id = fields.Many2one('hr.employee', string='Manager')
    start_date = fields.Datetime('Check IN')
    end_date = fields.Datetime('Check OUT')
    late_hours = fields.Float('Late Hours')
    notes = fields.Text(string='Notes')
    state = fields.Selection([('draft', 'Draft'), ('confirm', 'Waiting Approval'), ('refuse', 'To leave apply'), 
           ('validate', 'To Late Hours '), ('cancel', 'Cancelled')], default='draft', copy=False)
    attendance_id = fields.Many2one('hr.attendance', string='Attendance')
    
    @api.model
    def run_late_scheduler(self):
        current_date = date.today()
        working_hours_empl = self.env['hr.contract']
        attend_signin_ids = self.env['hr.attendance'].search([('late_created', '=', False)])
        for obj in attend_signin_ids:
            if obj.check_in:
                start_date_str = (str(obj.check_in))
                start_date = datetime.strptime(start_date_str,'%Y-%m-%d %H:%M:%S')
                con_set_date = datetime(start_date.year, start_date.month, start_date.day)+timedelta(hours=8)
                wk_day_check = datetime.strptime(start_date_str, DEFAULT_SERVER_DATETIME_FORMAT)+timedelta(hours=5,minutes=30)
                if wk_day_check > con_set_date:
                    difference = wk_day_check - con_set_date
                    hour_diff =int((difference.days) * 24 + (difference.seconds) / 3600)
                    min_diff = str(difference).split(':')[1]
                    tot_diff = str(hour_diff) + '.' + min_diff
                    total_late_h = float(tot_diff)
                    vals = {
                            'employee_id':obj.employee_id and obj.employee_id.id or False,
                            'manager_id' : obj.employee_id and obj.employee_id.parent_id and obj.employee_id.parent_id.id or False,
                            'start_date' : obj.check_in,
                            'end_date':obj.check_out,
                            'late_hours':round(total_late_h,2),
                            'attendance_id': obj.id,
                            }
                    self.env['codeso.hr.late'].create(vals)
                    obj.late_created = True
                    
    @api.multi
    def action_submit(self):
        return self.write({'state':'confirm'})
        
    @api.multi
    def action_cancel(self):
        return self.write({'state':'cancel'})
        
    @api.multi
    def action_approve(self):
        return self.write({'state':'validate'})
    
    @api.multi
    def action_refuse(self):
        return self.write({'state':'refuse'})
        
    @api.multi
    def action_view_attendance(self):
        attendances = self.mapped('attendance_id')
        action = self.env.ref('hr_attendance.hr_attendance_action').read()[0]
        if len(attendances) > 1:
            action['domain'] = [('id', 'in', attendances.ids)]
        elif len(attendances) == 1:
            action['views'] = [(self.env.ref('hr_attendance.hr_attendance_view_form').id, 'form')]
            action['res_id'] = self.attendance_id.id
        else:
            action = {'type': 'ir.actions.act_window_close'}
        return action
    
class HrAttendance(models.Model):
    _inherit = "hr.attendance" 
    
    late_created = fields.Boolean(string = 'Late Created', default=False, copy=False)
    


    
    
    
    
