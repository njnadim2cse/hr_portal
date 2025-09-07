from odoo import http
from odoo.http import request

class DashboardController(http.Controller):

    @http.route('/dashboard', type='http', auth='user', website=True)
    def dashboard_home(self, **kw):
        return request.render('hr_dashboard_updated.dashboard_main')

    @http.route('/dashboard/attendance', type='http', auth='user', website=True)
    def attendance_dashboard(self, **kw):
        employee = request.env['hr.employee'].search([('user_id', '=', request.env.user.id)], limit=1)
        if not employee:
            return "No employee linked to this user."
        data = request.env['attendance.dashboard'].sudo().get_attendance_data(employee.id)
        return request.render('hr_dashboard_updated.dashboard_attendance', {'data': data})

    @http.route('/dashboard/leave', type='http', auth='user', website=True)
    def leave_dashboard(self, **kw):
        employee = request.env['hr.employee'].search([('user_id', '=', request.env.user.id)], limit=1)
        if not employee:
            return "No employee linked to this user."
        
        data = request.env['leave.dashboard'].sudo().get_leave_data(employee.id)
        return request.render('hr_dashboard_updated.leave_dashboard_template', {'data': data})


    @http.route('/dashboard/loan_financial_aid', type='http', auth='user', website=True)
    def loan_financial_aid(self, **kw):
        employee = request.env['hr.employee'].search([('user_id', '=', request.env.user.id)], limit=1)
        if not employee:
            return "No employee linked to this user."

        # Fetch existing requests for this employee
        requests = request.env['loan.financial.aid'].sudo().search([('employee_id', '=', employee.id)], order='request_date desc')

        return request.render('hr_dashboard_updated.loan_financial_aid', {
            'employee': employee,
            'requests': requests
        })

    @http.route('/dashboard/loan_financial_aid/submit', type='http', auth='user', methods=['POST'], website=True)
    def submit_loan_request(self, **kw):
        employee = request.env['hr.employee'].search([('user_id', '=', request.env.user.id)], limit=1)
        if not employee:
            return "No employee linked to this user."

        loan_type = kw.get('loan_type')
        amount = kw.get('amount')
        guarantor_id = kw.get('guarantor_id')
        phone = kw.get('phone')

        request.env['loan.financial.aid'].sudo().create({
            'employee_id': employee.id,
            'loan_type': loan_type,
            'amount': amount,
            'guarantor_id': int(guarantor_id) if guarantor_id else False,
            'phone': phone,
        })

        return request.redirect('/dashboard/loan_financial_aid')

    @http.route('/dashboard/expenses', type='http', auth='user', website=True)
    def expenses(self, **kw):
        return request.render('hr_dashboard_updated.dashboard_expense')

    @http.route('/dashboard/about_me', type='http', auth='user', website=True)
    def about_me(self, **kw):
        return request.render('hr_dashboard_updated.db_aboutme')

