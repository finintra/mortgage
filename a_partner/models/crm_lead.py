from odoo import fields, models


class CrmLead(models.Model):
    _inherit = "crm.lead"

    def _compute_first_partner(self):
        if self.partner_id:
            self.first_partner = True
        else:
            self.first_partner = False

    partner_id_2 = fields.Many2one(
        'res.partner', string='Customer', check_company=True, index=True, tracking=10)
    email_from_2 = fields.Char(related="partner_id_2.email", readonly=False)
    phone_2 = fields.Char(related="partner_id_2.phone", readonly=False)

    first_partner = fields.Boolean(compute="_compute_first_partner")
    second_partner = fields.Boolean()

    empty_field = fields.Char(readonly=True)
    empty_field_2 = fields.Char(readonly=True)

    # default fields
    postcode = fields.Char(related="partner_id.postcode", readonly=False)
    contact_details = fields.Char(related="partner_id.contact_details")
    home = fields.Char(related="partner_id.home", readonly=False)
    office = fields.Char(related="partner_id.office", readonly=False)
    family_state = fields.Selection(related="partner_id.family_state", readonly=False)
    ni_number = fields.Char(related="partner_id.ni_number", readonly=False)
    date_of_birth = fields.Date(related="partner_id.date_of_birth", readonly=False)
    place_of_birth = fields.Char(related="partner_id.place_of_birth", readonly=False)
    children = fields.Text(related="partner_id.children", readonly=False)
    nationality = fields.Char(related="partner_id.nationality", readonly=False)
    residency = fields.Char(related="partner_id.residency", readonly=False)
    previous_addresses = fields.Text(related="partner_id.previous_addresses", readonly=False)
    sort_code = fields.Char(related="partner_id.sort_code", readonly=False)
    account_number = fields.Char(related="partner_id.account_number", readonly=False)
    account_name = fields.Char(related="partner_id.account_name", readonly=False)

    function = fields.Char(related="partner_id.function", readonly=False)
    emp_status = fields.Selection(related="partner_id.emp_status", readonly=False)
    employee_name = fields.Char(related="partner_id.employee_name", readonly=False)
    status = fields.Selection(related="partner_id.status")
    length_of_employment = fields.Char(related="partner_id.length_of_employment", readonly=False)
    probationary = fields.Boolean(related="partner_id.probationary", readonly=False)
    total_annual = fields.Float(related="partner_id.total_annual", readonly=False)
    addresses = fields.Text(related="partner_id.addresses", readonly=False)
    significant_details = fields.Text(related="partner_id.significant_details", readonly=False)
    last_3_years_income = fields.Float(related="partner_id.last_3_years_income", readonly=False)
    last_2_years_income = fields.Float(related="partner_id.last_2_years_income", readonly=False)
    last_1_years_income = fields.Float(related="partner_id.last_1_years_income", readonly=False)
    projected_earnings = fields.Float(related="partner_id.projected_earnings", readonly=False)
    projected_earnings_next = fields.Float(related="partner_id.projected_earnings_next", readonly=False)
    contract_years = fields.Integer(related="partner_id.contract_years", readonly=False)
    anticipate_changes = fields.Boolean(related="partner_id.anticipate_changes", readonly=False)
    description = fields.Text(related="partner_id.description", readonly=False)
    note = fields.Text(related="partner_id.note", readonly=False)
    planned_age = fields.Integer(related="partner_id.planned_age", readonly=False)
    is_happy = fields.Boolean(related="partner_id.is_happy", readonly=False)
    post_retirement = fields.Float(related="partner_id.post_retirement", readonly=False)
    assets = fields.Text(related="partner_id.assets", readonly=False)

    owner = fields.Selection(related="partner_id.owner", readonly=False)
    pur_date = fields.Date(related="partner_id.pur_date", readonly=False)
    pur_price = fields.Float(related="partner_id.pur_price", readonly=False)
    pur_current = fields.Float(related="partner_id.pur_current", readonly=False)
    mortgage = fields.Boolean(related="partner_id.mortgage", readonly=False)
    repayment_method = fields.Char(related="partner_id.repayment_method", readonly=False)
    lender = fields.Char(related="partner_id.lender", readonly=False)
    amount_outstanding = fields.Float(related="partner_id.amount_outstanding", readonly=False)
    term_remaining = fields.Char(related="partner_id.term_remaining", readonly=False)
    monthly_payment = fields.Char(related="partner_id.monthly_payment", readonly=False)
    interest_rate = fields.Char(related="partner_id.interest_rate", readonly=False)
    rate_type = fields.Char(related="partner_id.rate_type", readonly=False)
    transfer_penalty = fields.Char(related="partner_id.transfer_penalty", readonly=False)
    end_date = fields.Date(related="partner_id.end_date", readonly=False)
    ownership = fields.Char(related="partner_id.ownership", readonly=False)
    additional_notes = fields.Text(related="partner_id.additional_notes", readonly=False)
    monthly_rent = fields.Float(related="partner_id.monthly_rent", readonly=False)
    electoral = fields.Boolean(related="partner_id.electoral", readonly=False)
    tenancy_date = fields.Date(related="partner_id.tenancy_date", readonly=False)

    liabilities = fields.Many2many(related="partner_id.liabilities", readonly=False)
    liabilities_2 = fields.Many2many(related="partner_id_2.liabilities", readonly=False)

    function_2 = fields.Char(related="partner_id_2.function", readonly=False)
    emp_status_2 = fields.Selection(related="partner_id_2.emp_status", readonly=False)
    employee_name_2 = fields.Char(related="partner_id_2.employee_name", readonly=False)
    status_2 = fields.Selection(related="partner_id_2.status", readonly=False)
    length_of_employment_2 = fields.Char(related="partner_id_2.length_of_employment", readonly=False)
    probationary_2 = fields.Boolean(related="partner_id_2.probationary", readonly=False)
    total_annual_2 = fields.Float(related="partner_id_2.total_annual", readonly=False)
    addresses_2 = fields.Text(related="partner_id_2.addresses", readonly=False)
    significant_details_2 = fields.Text(related="partner_id_2.significant_details", readonly=False)
    last_3_years_income_2 = fields.Float(related="partner_id_2.last_3_years_income", readonly=False)
    last_2_years_income_2 = fields.Float(related="partner_id_2.last_2_years_income", readonly=False)
    last_1_years_income_2 = fields.Float(related="partner_id_2.last_1_years_income", readonly=False)
    projected_earnings_2 = fields.Float(related="partner_id_2.projected_earnings", readonly=False)
    projected_earnings_next_2 = fields.Float(related="partner_id_2.projected_earnings_next", readonly=False)
    contract_years_2 = fields.Integer(related="partner_id_2.contract_years", readonly=False)
    anticipate_changes_2 = fields.Boolean(related="partner_id_2.anticipate_changes", readonly=False)
    description_2 = fields.Text(related="partner_id_2.description", readonly=False)
    note_2 = fields.Text(related="partner_id_2.note", readonly=False)
    planned_age_2 = fields.Integer(related="partner_id_2.planned_age", readonly=False)
    is_happy_2 = fields.Boolean(related="partner_id_2.is_happy")
    post_retirement_2 = fields.Float(related="partner_id_2.post_retirement", readonly=False)
    assets_2 = fields.Text(related="partner_id_2.assets", readonly=False)

    owner_2 = fields.Selection(related="partner_id_2.owner", readonly=False)
    pur_date_2 = fields.Date(related="partner_id_2.pur_date", readonly=False)
    pur_price_2 = fields.Float(related="partner_id_2.pur_price", readonly=False)
    pur_current_2 = fields.Float(related="partner_id_2.pur_current", readonly=False)
    mortgage_2 = fields.Boolean(related="partner_id_2.mortgage", readonly=False)
    repayment_method_2 = fields.Char(related="partner_id_2.repayment_method", readonly=False)
    lender_2 = fields.Char(related="partner_id_2.lender", readonly=False)
    amount_outstanding_2 = fields.Float(related="partner_id_2.amount_outstanding", readonly=False)
    term_remaining_2 = fields.Char(related="partner_id_2.term_remaining", readonly=False)
    monthly_payment_2 = fields.Char(related="partner_id_2.monthly_payment", readonly=False)
    interest_rate_2 = fields.Char(related="partner_id_2.interest_rate", readonly=False)
    rate_type_2 = fields.Char(related="partner_id_2.rate_type", readonly=False)
    transfer_penalty_2 = fields.Char(related="partner_id_2.transfer_penalty", readonly=False)
    end_date_2 = fields.Date(related="partner_id_2.end_date", readonly=False)
    ownership_2 = fields.Char(related="partner_id_2.ownership", readonly=False)
    additional_notes_2 = fields.Text(related="partner_id_2.additional_notes", readonly=False)
    monthly_rent_2 = fields.Float(related="partner_id_2.monthly_rent", readonly=False)
    electoral_2 = fields.Boolean(related="partner_id_2.electoral", readonly=False)
    tenancy_date_2 = fields.Date(related="partner_id_2.tenancy_date", readonly=False)

    salary = fields.Float()
    overtime = fields.Float()
    bonus = fields.Float()
    benefits = fields.Float()
    investment = fields.Float()
    rental = fields.Float()
    other = fields.Float()
    annual = fields.Float()
    anticipate = fields.Boolean()
    if_yes = fields.Text()
    net_per_month = fields.Float()

    def _compute_total_expenses(self):
        for rec in self:
            rec.total_expenses = 0
            rec.total_expenses = (rec.rent + rec.investments + rec.repayments + rec.credit_cards + rec.household_bills
                                  + rec.council + rec.food_living + rec.insurances + rec.pensions + rec.ground_rent
                                  + rec.insurance + rec.school_fees + rec.childcare + rec.social_expenses
                                  + rec.social_expenses + rec.travel_expenses + rec.holidays + rec.other_expenses)

    rent = fields.Float()
    investments = fields.Float()
    repayments = fields.Float()
    credit_cards = fields.Float()
    household_bills = fields.Float()
    council = fields.Float()
    food_living = fields.Float()
    insurances = fields.Float()
    pensions = fields.Float()
    ground_rent = fields.Float()
    insurance = fields.Float()
    school_fees = fields.Float()
    childcare = fields.Float()
    social_expenses = fields.Float()
    travel_expenses = fields.Float()
    holidays = fields.Float()
    other_expenses = fields.Float()
    total_expenses = fields.Float(compute="_compute_total_expenses")
    note_expenses = fields.Text()

    reason = fields.Char()
    house_price = fields.Float()
    maximum_mortgage = fields.Float()
    available = fields.Float()
    repayments_required = fields.Float()
    source = fields.Char()
    add_to_loan = fields.Boolean()
    remortgaging = fields.Text()
    important = fields.Selection([("fixed", "Fixed monthly outgoing & ability to budget for a period"),
                                  ("variable",
                                   "Lowest initial payments. However, potential increase in monthly payments")])
    depending = fields.Char()
    indicate = fields.Char(readonly=True)
    no_redemption = fields.Selection([
        ("major", "Major"),
        ("minor", "Minor"),
        ("na", "N/A"),
    ])
    option_to_offset = fields.Selection([
        ("major", "Major"),
        ("minor", "Minor"),
        ("na", "N/A"),
    ])
    speed = fields.Selection([
        ("major", "Major"),
        ("minor", "Minor"),
        ("na", "N/A"),
    ])
    fee_free = fields.Selection([
        ("major", "Major"),
        ("minor", "Minor"),
        ("na", "N/A"),
    ])
    lowest_possible = fields.Selection([
        ("major", "Major"),
        ("minor", "Minor"),
        ("na", "N/A"),
    ])
    is_important = fields.Boolean()
    describe = fields.Text()

    tenure = fields.Selection([
        ("freehold", "Freehold"),
        ("leasehold", "Leasehold"),
    ])
    if_l_years = fields.Integer()
    type_of_property = fields.Selection([
        ("house", "House"),
        ("bungalow", "Bungalow"),
        ("flat", "Flat"),
        ("maisonette", "Maisonette"),
        ("other", "Other"),
    ])
    if_a_flat = fields.Char(readonly=True)
    above_shops = fields.Boolean()
    local_authority = fields.Boolean()
    number_of_floors = fields.Float()
    type_of_construction = fields.Selection([
        ("brick", "Brick"),
        ("stone", "Stone"),
        ("timber", "Timber Frame"),
        ("other", "Other"),
    ])
    year_of_construction = fields.Float()
    details = fields.Text()
    agent_details = fields.Text()

    from_1 = fields.Float()
    to_1 = fields.Float()
    over = fields.Char()
    no_longer = fields.Char()
    prior = fields.Text()

    do_you = fields.Selection([
        ("yes", "Yes. See below"),
        ("no", "No, I anticipate paying off this loan through the sale of the property(ies)"),
    ])
    if_you = fields.Boolean()
    if_you_2 = fields.Boolean()
    if_yes_2 = fields.Char()
    if_you_3 = fields.Selection([
        ("savings", "Savings"),
        ("switch", "Switch"),
        ("other", "Other"),
    ])
    details_risks = fields.Text()
    answers = fields.Selection([
        ("cautious", "Cautious"),
        ("balanced", "Balanced"),
        ("aggressive", "Aggressive"),
    ])

