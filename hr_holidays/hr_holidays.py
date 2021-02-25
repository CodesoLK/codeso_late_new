from flectra import fields, api, models, _
from datetime import date,datetime,timedelta
from ast import literal_eval
import time
from flectra.tools import DEFAULT_SERVER_DATETIME_FORMAT
from dateutil.relativedelta import relativedelta


class HrHolidays(models.Model):
    _inherit = 'hr.holidays'
    
    late_record = fields.Many2one('codeso.hr.holidays', String='late Record')

    @api.model
    def create(self, vals):
        if self.env.context.get('parent_id'):
            late_record_id = self.env.context.get('parent_id')
            late_record_object = self.env['codeso.hr.late'].browse([late_record_id])
            late_record_object.write({'state': 'refuse'})
            vals['late_record'] = self.env.context.get('parent_id')
        return super(HrHolidays, self).create(vals)