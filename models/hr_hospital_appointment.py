from odoo import models, fields, api, exceptions, _


class Appointment(models.Model):
    _name = 'hospital.appointment'
    _description = 'Doctor Appointment'

    doctor = fields.Many2one(
        comodel_name='hospital.doctor', required=True
    )
    patient = fields.Many2one(
        comodel_name='hospital.patient', required=True
    )
    planned_date = fields.Datetime(
        string='Planned Appointment Date and Time',
        required=True,
        help="Date and time when the appointment is scheduled."
    )
    actual_date = fields.Datetime(
        string='Actual Appointment Date and Time',
        help="Date and time when the appointment actually occurred."
    )
    status = fields.Selection(
        [
            ('planned', 'Planned'),
            ('done', 'Completed'),
            ('cancelled', 'Cancelled')
        ],
        default='planned',
        required=True
    )
    diagnosis_ids = fields.One2many(
        comodel_name='hospital.diagnosis',
        inverse_name='appointment_id',
        string='Diagnoses'
    )
    recommendations = fields.Text()
    is_done = fields.Boolean(string='Is Appointment Done', default=False)

    # Зміна `appointment_date` на `planned_date` (для ясності коду):
    @api.constrains('doctor', 'planned_date')
    def _check_duplicate_appointment(self):
        """Ensure there are no duplicate appointments for the same doctor
        at the same planned date."""
        for record in self:
            domain = [
                ('doctor', '=', record.doctor.id),
                ('planned_date', '=', record.planned_date),
                ('id', '!=', record.id)
            ]
            if self.search_count(domain) > 0:
                raise exceptions.ValidationError(_(
                    'An appointment with the same doctor '
                    'at this planned time already exists.'))

    @api.constrains('status', 'actual_date', 'planned_date', 'doctor')
    def _check_immutable_fields(self):
        """Prevent editing key fields if the appointment is marked as done."""
        for record in self:
            if record.status == 'done':
                if self.env.context.get('force_edit', False):
                    continue  # Allow modifications in special cases
                if any(field for field in ['doctor', 'planned_date']
                       if self[field] != record[field]):
                    raise exceptions.ValidationError(_(
                        'You cannot change the doctor '
                        'or planned date for an appointment '
                        'that has already been completed.'))

    @api.ondelete(at_uninstall=False)
    def _check_delete(self):
        """Prevent deletion of appointments with linked diagnoses."""
        for record in self:
            if record.diagnosis_ids:
                raise exceptions.UserError(_(
                    'You cannot delete appointments with linked diagnoses.'
                ))
