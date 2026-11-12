from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError

class Loan(models.Model):
    _name = "salf.loan"
    _description = "Financial Loan"
    _rec_name = "name"
    _order = "date desc, id desc"

    name = fields.Char(string="رقم السلفة", required=True, copy=False, default="جديد")
    customer_id = fields.Many2one("salf.customer", string="الزبون", required=True, ondelete="restrict", index=True)
    amount = fields.Monetary(string="مبلغ السلفة", required=True, currency_field="currency_id")
    currency_id = fields.Many2one("res.currency", string="العملة", default=lambda self: self.env.ref("base.IQD", raise_if_not_found=False) or self.env.company.currency_id)
    date = fields.Date(string="تاريخ السلفة", required=True, default=fields.Date.context_today)
    disbursement_state = fields.Selection(
        [("not_disbursed", "غير نازلة"), ("disbursed", "نازلة")],
        string="حالة النزول", default="not_disbursed", required=True
    )
    repayment_state = fields.Selection(
        [("unpaid", "غير مسددة"), ("paid", "مسددة بالكامل")],
        string="حالة التسديد", default="unpaid", required=True
    )
    disbursement_date = fields.Date(string="تاريخ صرف السلفة", readonly=True)
    repayment_date = fields.Date(string="تاريخ التسديد", readonly=True)
    notes = fields.Text(string="ملاحظات")

    _sql_constraints = [
        ("one_loan_per_customer", "unique(customer_id)", "لا يمكن تسجيل أكثر من سلفة واحدة للزبون نفسه."),
        ("positive_amount", "CHECK(amount > 0)", "يجب أن يكون مبلغ السلفة أكبر من صفر."),
    ]

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("name", "جديد") == "جديد":
                vals["name"] = self.env["ir.sequence"].next_by_code("salf.loan") or "سلفة"
        return super().create(vals_list)

    def action_disburse(self):
        for rec in self:
            if rec.disbursement_state == "disbursed":
                raise UserError(_("تم صرف هذه السلفة مسبقاً."))
            rec.write({
                "disbursement_state": "disbursed",
                "disbursement_date": fields.Date.context_today(self),
            })
        return self.env.ref("salf_management.action_report_disbursement_receipt").report_action(self)

    def action_repay(self):
        for rec in self:
            if rec.disbursement_state != "disbursed":
                raise UserError(_("لا يمكن تسديد سلفة لم يتم صرفها."))
            if rec.repayment_state == "paid":
                raise UserError(_("هذه السلفة مسددة مسبقاً."))
            rec.write({
                "repayment_state": "paid",
                "repayment_date": fields.Date.context_today(self),
            })
        return self.env.ref("salf_management.action_report_repayment_receipt").report_action(self)

    def action_print_disbursement(self):
        self.ensure_one()
        return self.env.ref("salf_management.action_report_disbursement_receipt").report_action(self)

    def action_print_repayment(self):
        self.ensure_one()
        if self.repayment_state != "paid":
            raise UserError(_("لا يوجد وصل تسديد قبل تسجيل التسديد."))
        return self.env.ref("salf_management.action_report_repayment_receipt").report_action(self)
