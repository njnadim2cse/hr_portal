from odoo import models, fields, api

class LoanFinancialAid(models.Model):
    _name = "loan.financial.aid"
    _description = "Loan & Financial Aid Requests"

    employee_id = fields.Many2one('hr.employee', string="Employee", required=True)
    loan_type = fields.Selection([
        ('personal', 'Personal'),
        ('education', 'Education'),
        ('medical', 'Medical'),
        ('other', 'Other')
    ], string="Loan Type", required=True)
    amount = fields.Float(string="Amount", required=True)
    guarantor_id = fields.Many2one('hr.employee', string="Guarantor Employee")
    phone = fields.Char(string="Phone Number")
    state = fields.Selection([
        ('to_approve', 'To Approve'),
        ('approved', 'Approved'),
        ('refused', 'Refused')
    ], default='to_approve', string="Status")
    request_date = fields.Datetime(string="Request Date", default=fields.Datetime.now)
