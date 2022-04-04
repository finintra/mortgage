from odoo import fields, models


class Partner(models.Model):
    _inherit = "res.partner"

    postcode = fields.Char()
    contact_details = fields.Char(readonly=True)
    home = fields.Char()
    office = fields.Char()
    family_state = fields.Selection([
        ('single', 'Single'),
        ('married', 'Married'),
        ('divorced', 'Divorced'),
        ('widowed', 'Widowed'),
        ('separated', 'Separated'),
        ('life_partner', 'Life Partner'),
    ])
    ni_number = fields.Char()
    date_of_birth = fields.Date()
    place_of_birth = fields.Char()
    children = fields.Text()
    nationality = fields.Char()
    residency = fields.Char()
    previous_addresses = fields.Text()
    empty_field = fields.Char(readonly=True)
    sort_code = fields.Char()
    account_number = fields.Char()
    account_name = fields.Char()

    emp_status = fields.Selection([
        ('self_employed', 'Self-Employed'),
        ('employed', 'Employed'),
        ('combination', 'Combination')
    ])
    employee_name = fields.Char()
    status = fields.Selection([
        ('contract', 'Contract'),
        ('full_time', 'Full-time')
    ])
    length_of_employment = fields.Char()
    probationary = fields.Boolean()
    total_annual = fields.Float()
    addresses = fields.Text()
    significant_details = fields.Text()
    last_3_years_income = fields.Float()
    last_2_years_income = fields.Float()
    last_1_years_income = fields.Float()
    projected_earnings = fields.Float()
    projected_earnings_next = fields.Float()
    contract_years = fields.Integer()
    anticipate_changes = fields.Boolean()
    description = fields.Text()
    note = fields.Text()
    planned_age = fields.Integer()
    is_happy = fields.Boolean()
    post_retirement = fields.Float()
    assets = fields.Text()

    owner = fields.Selection([
        ('owner_occupier', 'Owner/Occupier'),
        ('renting', 'Renting'),
        ('living_with_parents', "Living with parents")
    ])
    pur_date = fields.Date()
    pur_price = fields.Float()
    pur_current = fields.Float()
    mortgage = fields.Boolean()
    repayment_method = fields.Char()
    lender = fields.Char()
    amount_outstanding = fields.Float()
    term_remaining = fields.Char()
    monthly_payment = fields.Float()
    interest_rate = fields.Char()
    rate_type = fields.Char()
    transfer_penalty = fields.Char()
    end_date = fields.Date()
    ownership = fields.Char()
    additional_notes = fields.Text()
    monthly_rent = fields.Float()
    electoral = fields.Boolean()
    tenancy_date = fields.Date()

    liabilities = fields.One2many("liabilities", "partner_ids", reanonly=False)
