from odoo import fields, models

class SalfDashboard(models.TransientModel):
    _name = "salf.dashboard"
    _description = "لوحة مؤشرات السلف"

    customer_count = fields.Integer(string="عدد الزبائن", compute="_compute_counts")
    disbursed_count = fields.Integer(string="السلف النازلة", compute="_compute_counts")
    not_disbursed_count = fields.Integer(string="السلف غير النازلة", compute="_compute_counts")
    unpaid_count = fields.Integer(string="السلف المتبقية", compute="_compute_counts")
    paid_count = fields.Integer(string="السلف المسددة بالكامل", compute="_compute_counts")

    def _compute_counts(self):
        Customer = self.env["salf.customer"]
        Loan = self.env["salf.loan"]
        for rec in self:
            rec.customer_count = Customer.search_count([])
            rec.disbursed_count = Loan.search_count([("disbursement_state", "=", "disbursed")])
            rec.not_disbursed_count = Loan.search_count([("disbursement_state", "=", "not_disbursed")])
            rec.unpaid_count = Loan.search_count([("repayment_state", "=", "unpaid")])
            rec.paid_count = Loan.search_count([("repayment_state", "=", "paid")])
