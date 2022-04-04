from odoo import fields, models


class Liabilities(models.Model):
    _name = "liabilities"

    name = fields.Char(required=True)
    owner_applicant = fields.Char()
    type_applicant = fields.Char()
    lender_applicant = fields.Char()
    balance_applicant = fields.Char()
    monthly_applicant = fields.Char()
    end_date_applicant = fields.Date()
    mortgage_applicant = fields.Char()
    costs_associated = fields.Boolean()
    possible_consequences = fields.Boolean()
    judgments = fields.Boolean()
    settled = fields.Boolean()
    bankrupt = fields.Boolean()
    discharged = fields.Boolean()
    associated_notes = fields.Text()
    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id, required=True)
    partner_ids = fields.Char(readonly=True, string="", default="")
