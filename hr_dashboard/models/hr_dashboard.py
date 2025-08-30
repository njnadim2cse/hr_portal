from odoo import models, api
from datetime import datetime, time

class HrDashboard(models.Model):
    _name = 'hr.dashboard'
    _description = 'HR Dashboard Data'

    @api.model
    def get_attendance_data(self, employee_id, start_date, end_date):
        attendance_records = self.env['hr.attendance'].search([
            ('employee_id', '=', employee_id),
            ('check_in', '>=', start_date),
            ('check_out', '<=', end_date)
        ])

        data = []
        for att in attendance_records:
            data.append({
                'date': att.check_in.date(),
                'status': self._get_status(att.check_in),
                'check_in': att.check_in,
                'check_out': att.check_out,
                'worked_hours': self._format_worked_hours(att.worked_hours),
            })
        return data

    def _get_status(self, check_in):
        """Return Present, Late or Absent based on check-in time"""
        if not check_in:
            return 'Absent'

        cutoff_time = time(9, 15)  # 9:15 AM
        if check_in.time() > cutoff_time:
            return 'Late'
        else:
            return 'Present'

    def _format_worked_hours(self, hours):
        """Convert float hours to HH:MM format"""
        if not hours:
            return "00:00"
        h = int(hours)
        m = int((hours - h) * 60)
        return f"{h:02d}:{m:02d}"

    @api.model
    def get_summary(self, employee_id, month):
        start_date = month + '-01'
        end_date = month + '-31'

        records = self.env['hr.attendance'].search([
            ('employee_id', '=', employee_id),
            ('check_in', '>=', start_date),
            ('check_in', '<=', end_date)
        ])

        total_days = len(records)
        late_days = sum(1 for rec in records if rec.check_in.time() > time(9, 15))

        return {
            'month': month,
            'present': total_days - late_days,
            'late_days': late_days,
            'absent': 31 - total_days,  # assuming 31 days max
        }
