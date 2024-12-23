from odoo import models, fields, api, exceptions, _


class Doctor(models.Model):
    _name = 'hospital.doctor'
    _description = 'Doctor'

    # Basic information about the doctor
    name = fields.Char(string='Full Name',
                       required=True)  # Doctor's name (required)
    date_of_birth = fields.Date(string='Date of Birth')  # Date of birth
    gender = fields.Selection(selection=[
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ], string='Gender')  # Doctor's gender
    phone = fields.Char(string='Phone Number')  # Phone number

    # Doctor's specialization
    specialization = fields.Char(
        string='Specialization', required=True)  # Specialization (required)
    intern = fields.Many2one(comodel_name='hospital.doctor', string='Intern'
                             )  # Intern (linked record)
    mentor = fields.Many2one(comodel_name='hospital.doctor',
                             string='Mentor')  # Mentor (linked record)

    @api.constrains('intern', 'mentor')
    def _check_mentor_intern(self):
        """Ensure the intern and mentor are not the same person."""
        for record in self:
            if record.intern and record.intern == record.mentor:
                raise exceptions.ValidationError(
                    _("The intern cannot be their own mentor.")
                )

    @api.model_create_multi
    def create(self, vals):
        """Record creation method."""
        return super(Doctor, self).create(vals)

    def write(self, vals):
        """Record editing method."""
        return super(Doctor, self).write(vals)
