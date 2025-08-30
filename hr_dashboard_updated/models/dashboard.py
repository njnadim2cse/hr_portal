from collections import defaultdict
from datetime import datetime, timedelta, time
import calendar
from pytz import timezone, UTC
from odoo import models, api


class AttendanceDashboard(models.Model):
    _name = 'attendance.dashboard'
    _description = 'Attendance Dashboard'

    @api.model
    def get_attendance_data(self, employee_id):
        employee = self.env['hr.employee'].browse(employee_id)
        user_tz = timezone(self.env.user.tz or 'UTC')

        today = datetime.now(UTC).astimezone(user_tz).date()
        start_date = today.replace(day=1)
        # Last day of month
        next_month = start_date + timedelta(days=32)
        end_date = next_month.replace(day=1) - timedelta(days=1)

        # Get attendance records for this employee in the month
        attendances = self.env['hr.attendance'].search([
            ('employee_id', '=', employee.id),
            ('check_in', '>=', datetime.combine(start_date, time.min).astimezone(UTC)),
            ('check_in', '<=', datetime.combine(end_date, time.max).astimezone(UTC)),
        ])

        # Group attendances by date
        daily_records = defaultdict(list)
        for att in attendances:
            if att.check_in:
                check_in_local = att.check_in.astimezone(user_tz)
                daily_records[check_in_local.date()].append(att)

        # Initialize response data
        data = {
            'employee': employee.name,
            'joining_date': employee.create_date.astimezone(user_tz).strftime("%d %b, %Y"),
            'present': 0,
            'late': 0,
            'absent': 0,
            'offday': 0,
            'total_extra_hours': 0,
            'days': []
        }

        # Rules
        late_threshold = time(9, 15)
        start_time = time(9, 0)
        end_time = time(18, 0)

        # Iterate over every day of month
        day = start_date
        while day <= end_date:
            records = daily_records.get(day, [])
            first_in, last_out = None, None
            work_hours, extra_hours = 0, 0
            status = "Absent"

            if records:
                # Convert times for that day
                check_ins = [r.check_in.astimezone(user_tz) for r in records if r.check_in]
                check_outs = [r.check_out.astimezone(user_tz) for r in records if r.check_out]

                if check_ins:
                    first_in = min(check_ins)
                if check_outs:
                    last_out = max(check_outs)

                if first_in and last_out:
                    delta = last_out - first_in
                    work_hours = round(delta.total_seconds() / 3600, 2)

                # Friday special case
                if day.weekday() == calendar.FRIDAY:
                    status = "Offday"
                    extra_hours = work_hours  # all hours count as extra
                    if work_hours > 0:
                        data['offday'] += 1
                else:
                    if first_in:
                        if first_in.time() > late_threshold:
                            status = "Late"
                            data['late'] += 1
                        else:
                            status = "Present"
                            data['present'] += 1
                    else:
                        status = "Absent"
                        data['absent'] += 1

                    # Extra hours (non-Friday)
                    if first_in and last_out:
                        if first_in.time() < start_time:
                            delta = datetime.combine(day, start_time, tzinfo=user_tz) - first_in
                            extra_hours += round(delta.total_seconds() / 3600, 2)
                        if last_out.time() > end_time:
                            delta = last_out - datetime.combine(day, end_time, tzinfo=user_tz)
                            extra_hours += round(delta.total_seconds() / 3600, 2)
            else:
                # No attendance records
                if day.weekday() == calendar.FRIDAY:
                    status = "Offday"
                    data['offday'] += 1
                else:
                    status = "Absent"
                    data['absent'] += 1

            # Add totals
            data['total_extra_hours'] += extra_hours

            # Append daily record
            data['days'].append({
                'date': day.strftime("%d %b, %Y"),
                'check_in': first_in.strftime("%H:%M") if first_in else "-",
                'check_out': last_out.strftime("%H:%M") if last_out else "-",
                'hours': work_hours,
                'extra_hours': extra_hours,
                'status': status,
            })

            day += timedelta(days=1)

        # Sort days (latest first)
        data['days'] = sorted(data['days'], key=lambda d: datetime.strptime(d['date'], "%d %b, %Y"), reverse=True)

        return data
