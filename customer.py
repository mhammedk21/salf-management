from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

class LoanCustomer(models.Model):
    _name = "salf.customer"
    _description = "Loan Customer"
    _rec_name = "name"
    _order = "name"

    name = fields.Char(string="اسم الزبون", required=True, index=True)
    phone = fields.Char(string="رقم الهاتف", index=True)
    qi_card_number = fields.Char(string="رقم بطاقة Qi", groups="salf_management.group_loan_manager,salf_management.group_loan_staff")
    address = fields.Text(string="عنوان الزبون")
    job_status = fields.Char(string="الوظيفة والحالة")
    referred_by = fields.Char(string="من طرف الأستاذ")
    loan_id = fields.Many2one("salf.loan", string="السلفة", readonly=True, copy=False)
    loan_count = fields.Integer(compute="_compute_loan_count", string="عدد السلف")

    @api.depends("loan_id")
    def _compute_loan_count(self):
        for rec in self:
            rec.loan_count = 1 if rec.loan_id else 0

    def action_view_loan(self):
        self.ensure_one()
        if not self.loan_id:
            return {
                "type": "ir.actions.act_window",
                "name": _("إنشاء سلفة"),
                "res_model": "salf.loan",
                "view_mode": "form",
                "context": {"default_customer_id": self.id},
                "target": "current",
            }
        return {
            "type": "ir.actions.act_window",
            "name": _("السلفة"),
            "res_model": "salf.loan",
            "view_mode": "form",
            "res_id": self.loan_id.id,
            "target": "current",
        }
