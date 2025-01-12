from odoo import models, fields, api, exceptions, _


class Doctor(models.Model):
    _name = 'hospital.doctor'
    _inherit = 'hr.hospital.person'
    _description = 'Doctor'

    # Doctor's specialization (Selection)
    specialization = fields.Selection(
        selection=[
            ('cardiologist', 'Cardiologist'),
            ('neurologist', 'Neurologist'),
            ('pediatrician', 'Pediatrician'),
            ('general_practitioner', 'General Practitioner'),
            ('surgeon', 'Surgeon'),
        ],
        required=True,
        help='Specialization of the doctor'
    )
    is_intern = fields.Boolean(string='Intern', default=False)
    mentor_id = fields.Many2one(
        comodel_name='hospital.doctor',
        string='Mentor',
        help='Mentor for the intern',
        domain="[('is_intern', '=', False)]"
    )
    intern_ids = fields.One2many(
        comodel_name='hospital.doctor',
        inverse_name='mentor_id',
        string='Interns'
    )

    @api.constrains('mentor_id', 'is_intern')
    def _check_mentor_and_intern(self):
        """Ensure the intern is not their own mentor."""
        for record in self:
            if record.is_intern and not record.mentor_id:
                raise exceptions.ValidationError(
                    _("An intern must have a mentor assigned.")
                )
            if record.mentor_id == record:
                raise exceptions.ValidationError(
                    _("An intern cannot be their own mentor.")
                )

    @api.constrains('mentor_id')
    def _check_mentor_not_intern(self):
        """Ensure the mentor is not an intern."""
        for record in self:
            if record.mentor_id and record.mentor_id.is_intern:
                raise exceptions.ValidationError(
                    _("A mentor cannot be an intern.")
                )
