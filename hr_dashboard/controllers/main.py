from odoo import http
from odoo.http import request
from datetime import datetime

class HrDashboardController(http.Controller):

    @http.route('/hr_dashboard/attendance/view', auth='user')
    def attendance_view(self, employee_id=None, start_date=None, end_date=None):
        if not employee_id:
            employee_id = request.env.user.employee_id.id

        # Default to current month if not provided
        if not start_date or not end_date:
            today = datetime.today()
            start_date = today.replace(day=1).strftime('%Y-%m-%d 00:00:00')
            end_date = today.strftime('%Y-%m-%d 23:59:59')

        data = request.env['hr.dashboard'].sudo().get_attendance_data(employee_id, start_date, end_date)
        return request.render('hr_dashboard.attendance_template', {
            'attendances': data
        })

    @http.route('/hr_dashboard/summary/view', auth='user')
    def summary_view(self, employee_id=None, month=None):
        if not employee_id:
            employee_id = request.env.user.employee_id.id

        if not month:
            month = datetime.today().strftime('%Y-%m')

        summary = request.env['hr.dashboard'].sudo().get_summary(employee_id, month)
        return request.render('hr_dashboard.summary_template', {
            'summary': summary
        })
