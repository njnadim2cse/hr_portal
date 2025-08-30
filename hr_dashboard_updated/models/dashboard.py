from collections import defaultdict
from datetime import datetime, timedelta
from pytz import timezone, UTC
from odoo import models, api

class AttendanceDashboard(models.Model):
    _name = 'attendance.dashboard'
    _description = 'Attendance Dashboard'

    @api.model
    def get_attendance_data(self, employee_id):
        employee = self.env['hr.employee'].browse(employee_id)
        user_tz = timezone(self.env.user.tz or 'UTC')

        today = datetime.today().date()
        start_date = today.replace(day=1)
        end_date = (start_date + timedelta(days=31)).replace(day=1) - timedelta(days=1)

        attendances = self.env['hr.attendance'].search([
            ('employee_id', '=', employee.id),
            ('check_in', '>=', start_date),
            ('check_in', '<=', end_date)
        ])

        data = {
            'employee': employee.name,
            'joining_date': employee.create_date.astimezone(user_tz).strftime("%d %b, %Y"),
            'present': 0,
            'late': 0,
            'absent': 0,
            'days': []
        }

        # --- Group attendances by date ---
        daily_records = defaultdict(list)
        for att in attendances:
            if att.check_in:
                check_in_local = att.check_in.replace(tzinfo=UTC).astimezone(user_tz)
                daily_records[check_in_local.date()].append(att)

        for day, records in daily_records.items():
            # Get earliest check_in and latest check_out for this day
            check_ins = [
                r.check_in.replace(tzinfo=UTC).astimezone(user_tz) for r in records if r.check_in
            ]
            check_outs = [
                r.check_out.replace(tzinfo=UTC).astimezone(user_tz) for r in records if r.check_out
            ]

            first_in = min(check_ins) if check_ins else None
            last_out = max(check_outs) if check_outs else None

            work_hours = 0
            if first_in and last_out:
                delta = last_out - first_in
                work_hours = round(delta.total_seconds() / 3600, 2)

            # Determine status
            status = 'Present'
            if first_in and first_in.hour > 9:
                status = 'Late'
                data['late'] += 1
            elif not first_in:
                status = 'Absent'
                data['absent'] += 1
            else:
                data['present'] += 1

            data['days'].append({
                'date': day,
                'check_in': first_in.strftime("%H:%M") if first_in else "-",
                'check_out': last_out.strftime("%H:%M") if last_out else "-",
                'hours': work_hours,
                'status': status,
            })

        # Sort days in descending order
        data['days'] = sorted(data['days'], key=lambda d: d['date'], reverse=True)

        return data
