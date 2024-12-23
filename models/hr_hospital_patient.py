from datetime import date
from odoo import models, fields, api


class Patient(models.Model):
    _name = 'hospital.patient'
    _description = 'Patient'

    # Basic information about the patient
    name = fields.Char(string='Full Name', required=True)  # Patient's name
    birth_date = fields.Date(string='Date of Birth',
                             required=True)  # Date of birth
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ], string='Gender', required=True)  # Patient's gender
    phone = fields.Char(string='Phone Number')  # Phone number

    # Field for age, computed automatically
    age = fields.Integer(string='Age', compute='_compute_age', store=True)

    # Patient's passport data
    passport_data = fields.Char(string='Passport Data')

    # Related contact (another patient)
    related_contact = fields.Many2one(
        comodel_name='hospital.patient',
        string='Related Contact',
        help="Select a related contact from other patients",
        domain="[('id', '!=', id)]",  # Prevents selecting the same patient
        context={'no_create': True}  # Disables creating a new record
    )

    # Doctor assigned to the patient
    doctor = fields.Many2one(
        comodel_name='hospital.doctor',
        string='Personal Doctor'
    )

    # Patient's disease type
    disease_type_id = fields.Many2one(
        comodel_name='hospital.disease.type',
        string='Disease Type',
        help='Disease the patient is suffering from'
    )

    @api.depends('birth_date')
    def _compute_age(self):
        """Calculate age based on the date of birth."""
        for record in self:
            if record.birth_date:
                today = date.today()
                birth_date = record.birth_date
                record.age = today.year - birth_date.year - (
                    (today.month, today.day) < (birth_date.month,
                                                birth_date.day)
                )
            else:
                record.age = 0
