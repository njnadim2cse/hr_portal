from odoo import http
from odoo.http import request

class AttendanceDashboardController(http.Controller):

    @http.route('/attendance/dashboard', type='http', auth='user', website=True)
    def attendance_dashboard(self, **kw):
        employee = request.env['hr.employee'].search([('user_id', '=', request.env.user.id)], limit=1)
        if not employee:
            return "No employee linked to this user."

        data = request.env['attendance.dashboard'].get_attendance_data(employee.id)
        return request.render('hr_dashboard_updated.dashboard_template', {'data': data})
